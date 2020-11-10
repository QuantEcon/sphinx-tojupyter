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

To install the extension:

```{code-block} bash
pip install sphinx-tojupyter
```

to upgrade your current installation to the latest version:

```{code-block} bash
pip install --upgrade sphinx-tojupyter
```

```{todo}
# Todo

Add installation to distribute via conda-forge.
See Issue [#160](https://github.com/QuantEcon/sphinx-tojupyter/issues/160).

```

You can refer to the [release notes](https://github.com/QuantEcon/sphinx-tojupyter/releases)
for information on each release.

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

