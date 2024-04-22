# Sortie

[![PyPI version](https://badge.fury.io/py/sortie.svg)](https://badge.fury.io/py/sortie)

An opinionated tool for formatting your `pyproject.toml` files. Built in Rust and based on
[taplo](https://github.com/tamasfe/taplo).

**Should you use this?**

Generally, using [taplo](https://github.com/tamasfe/taplo) would probably be more suitable for the typical
workflow. The primary purpose of this Python package is to facilitate easy integration with Python-based CI/CD pipelines
solely for formatting `pyproject.toml` files.

## Usage

```
$ sortie
pyproject.toml left unchanged.
```

Or, with the `--check` argument as part of your CI/CD pipeline:

```
$ sortie --check
pyproject.toml would be formatted!
```

## Options

You can modify the behavior of the formatter by setting the configuration in your `pyproject.toml`
file. _Sortie_ utilizes the `[tool.sortie]` section of your file. For full options, refer to
[formatter options](https://taplo.tamasfe.dev/configuration/formatter-options.html). Compared with
Taplo, by default, `reorder_arrays = true` and `reorder_keys = true` are automatically set.

Here is an example `pyproject.toml` file:

```toml
[tool.sortie]
reorder_arrays = true
reorder_keys = true
```
