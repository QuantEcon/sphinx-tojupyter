---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(installation)=
# Installation

```{note}
**Version 1.0** focuses on notebook generation. For execution, PDF, or HTML features, 
also install [Jupyter Book](https://jupyterbook.org/): `pip install jupyter-book`
```

## Requirements

- Python >= 3.11
- Sphinx >= 7.0

## Installation

Install via pip:

```bash
pip install sphinx-tojupyter
```

To upgrade to the latest version:

```bash
pip install --upgrade sphinx-tojupyter
```

## Optional Features

For enhanced functionality, install optional dependencies:

```bash
# MyST-NB glue support
pip install myst-nb

# sphinx-proof support
pip install sphinx-proof
```

## Release Notes

See the [release notes](https://github.com/QuantEcon/sphinx-tojupyter/releases) 
and [CHANGELOG](https://github.com/QuantEcon/sphinx-tojupyter/blob/main/CHANGELOG.md) 
for version information.

## Migration from v1.x

If upgrading from v1.x, see the [migration guide](https://github.com/QuantEcon/sphinx-tojupyter/blob/main/MIGRATION.md).

## Alternative

Another way to get the **latest** version it is to install directly
by getting a copy of the [repository](https://github.com/QuantEcon/sphinx-tojupyter):

```{code-block} bash
git clone https://github.com/QuantEcon/sphinx-tojupyter
```

and then use

```{code-block} bash
python setup.py install
```

## Developers

For developers it can be useful to install using the develop option:

```{code-block} bash
python setup.py develop
```

this will install the package into the site-wide package directory which is linked to
the code in your local copy of the repository. It is **not** recommended to install this
way for common use.

