"""
A class to manage configuration.

It can read a yaml or json file, then parse env vars to find the ones
starting with a prefix and can add/override values
"""
import json
import yaml
import os
import typing as t
import errno
from .utilities import dictObj


def yaml_load(fd):
    """
    Utility to load a yaml file
    """
    return yaml.load(fd, Loader=yaml.Loader)


class Configuration(dictObj):

    def __init__(self,
                 defaults: dict[str, t.Any] = {},
                 env_prefix: str | None = None,
                 configfile: str | None = None,
                 file_loader: t.Callable[[t.IO[t.Any]],
                                         t.Mapping[str, t.Any]] = yaml_load):
        """
        Create a configuration, as a dict.
        Can create it from:
            - a default dict passed at init;
            - environment variables, prefixed with a specific string;
            - a yaml or json file;

        Methods:
            - from_environ: reads config from environment variables;
            - from_file: loads and parses a file;
            - from_mapping: update the dict with a mapping (dict);

            - from_json: calls from_file using json parser;
            - from_yaml: calls from_file using yaml parser;
        """
        super().__init__(defaults or {})

        if env_prefix:
            self.from_environ(prefix=env_prefix)

        if configfile:
            self.from_file(filename=configfile,
                           load=file_loader)

    def from_environ(self,
                     prefix: str = "APP_CONFIG",
                     loads: t.Callable[[str], t.Any] = json.loads) -> bool:
        """
        Loads configuration parsing environment variables.
        Prefix is the prefix of the variables (that will be stripped).
        Variables can build structures, using `__` as separator
        between the levels.

        Examples:
            - `PREFIX_ANSWER=42` -> `answer`: 42
            - `PREFIX_A__B=1` -> `{'a': {'b': 1}}`
        """
        prefix = f"{prefix}_"
        len_prefix = len(prefix)

        for key in sorted(os.environ):
            if not key.startswith(prefix):
                continue
            value = os.environ[key]
            try:
                value = loads(value)
            except Exception:
                # Keep the value as a string if loading failed.
                pass

            key = key[len_prefix:].lower()

            if "__" not in key:
                # A non-nested key, set directly.
                self[key] = value
                continue

            current = self
            *parts, tail = key.split('__')

            for part in parts:
                if part not in current.keys():
                    current[part] = {}
                current = current[part]
            current[tail] = value

        return True

    def from_file(self,
                  filename: str | os.PathLike[str],
                  load: t.Callable[[t.IO[t.Any]], t.Mapping[str, t.Any]],
                  silent: bool = False,
                  text: bool = True,) -> bool:
        """
        Loads and parses a file, updating the config with the content.
        Wants a `load` method to use to parse the file.

        - `silent`: do not stop if file does not exist;
        - `text`: open file as text if True, as binary if False

        Example:
            conf.from_file('conf.json', load=json.load)
        NOTE:
            to open YAML file, we can use yaml.load, but that requires an extra
            parameter `Loader`.
            We have a simple function called `load_yaml` to use,
            so you can use `conf=c.from_file('config.yaml', load=yaml_load)`
        """

        try:
            with open(filename, "r" if text else "rb") as f:
                obj = load(f)
        except OSError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = f"Unable to load configuration file ({e.strerror})"
            raise

        return self.from_mapping(obj)

    def from_yaml(self,
                  filename: str | os.PathLike[str],
                  silent: bool = False,
                  text: bool = True) -> bool:
        """
        Syntax sugar to load a YAML file
        """
        return self.from_file(filename,
                              silent=silent,
                              text=text,
                              load=yaml_load)

    def from_json(self,
                  filename: str | os.PathLike[str],
                  silent: bool = False,
                  text: bool = True) -> bool:
        """
        Syntax sugar to load a JSON file
        """
        return self.from_file(filename,
                              silent=silent,
                              text=text,
                              load=json.load)

    def from_mapping(
        self, mapping: t.Mapping[str, t.Any] | None = None, **kwargs: t.Any
    ) -> bool:
        """Updates the config like :meth:`update`

        :return: Always returns ``True``.

        """
        mappings: dict[str, t.Any] = {}
        if mapping is not None:
            mappings.update(mapping)
        mappings.update(kwargs)
        self.update(mappings)
        return True


if __name__ == "__main__":
    os.environ['XX_TEST_SNAKE'] = "snakepit"  # test_snake: "snakepit"
    os.environ['XX__TEST_SKO'] = "rpion"  # _test_sko: "rpion"
    # test: {"a": {"b": {"c": "two levels"}}}
    os.environ['XX_TEST__A__B__C'] = "two levels"
    # test: {"a": {"b": {"d": "one levels"}}}
    os.environ['XX_TEST__A__B__D'] = "one level"

    c = Configuration(defaults=dict(a=1, b=2))
    c.from_file('config.yaml', load=yaml_load, silent=True)
    c.from_environ(prefix="XX")
