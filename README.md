# Vedro Dependency Finder

Plugin helps to find dependencies of unstable tests by shuffling selected tests

## Installation

```shell
$ pip3 install vedro-dependency-finder
```

## Usage

```python
import vedro
import vedro_dependency_finder as df


class Config(vedro.Config):
    class Plugins(vedro.Config.Plugins):
        class DependencyFinder(df.DependencyFinder):
            enabled = True

```

```shell
$ vedro run --dependency-finder scenarios/your_scenario.py
```
