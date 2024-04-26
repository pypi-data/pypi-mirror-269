"""
Collection of utilities, shortcuts and syntactic sugar
"""
from functools import singledispatchmethod
from typing import Any


class dictObj(dict):
    """
    A dict on steroids
    You can access keys as attributes

    :param init: a dict of initial values

    Example:

        >> c=Config({'a': 1, 'b': 2})
        >> c.a == c['a'] -> True
    """

    def __init__(self, init: dict | None) -> None:
        if init:
            for key, value in init.items():
                self.__parse_value(key, value)

    @singledispatchmethod
    def __parse_value(self, key: str, value: dict) -> None:
        super().__setitem__(key, dictObj(value))

    @__parse_value.register
    def _(self, key: str, value: list) -> None:
        for el in value:
            if type(el) is dict:
                el = dictObj(el)
            if key not in self:
                super().__setitem__(key, [el])
            else:
                self[key].append(el)

    @__parse_value.register
    def _(self, key: str, value: int | float | str) -> None:
        super().__setitem__(key, value)

    def __setitem__(self, item: str, value: Any) -> None:
        self.__parse_value(item, value)

    def __getitem__(self, item: str) -> None:
        return super().__getitem__(item)

    def __setattr__(self, key: str, value: Any) -> None:
        self.__parse_value(key, value)

    def __getattr__(self, key: str) -> None:
        if key in self:
            return self.get(key)
        else:
            raise KeyError(key)

    def __setstate__(self, items: dict = {}) -> None:
        for key, value in items.items():
            if type(value) is dictObj:
                setattr(self, key, value)

    def __getstate__(self) -> dict:
        el = dict()
        for key, value in self.items():
            if type(value) is dictObj:
                el[key] = dict(value)
            else:
                el[key] = value
        return el

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__parse_value(key, value)


if __name__ == "__main__":
    d = dictObj({'a': 1, 'b': {'c': 3, 'd': 4}})
