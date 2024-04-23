## SCRIPTONITE

A Python toolkit for scripting

## Introduction

When writing python utilites and CLI scripts there are some parts that need to be implented each time, like

- logging;
- configuration parsing;
- other nice to have;

We wrote some standard implementations, that gives enough flexibility, but reduce the effort required to start writing the core parts of our script.

More details on each submodule can be found in the `docs/` directory of the original repository.

### Install

```
pip intall scriptonite
```

or

clone the original repo, then run

```
poetry update
poetry build
```

then you can install from local copy, that you can find in `dist/` directory

### How to use

#### Logging

```
from scriptonite.logging import Logger

log = Logger()

log.info('Hello World!')
```

#### Configuration

```
from scriptonite.configuration import Configuration

configuration = Configuration(configfile="config.yaml",
                              env_prefix="MYCONFIG")

```
