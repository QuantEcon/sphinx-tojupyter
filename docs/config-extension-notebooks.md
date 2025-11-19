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

(config_extension_notebooks)=
# Constructing Jupyter Notebooks

```{note}
**Version 1.0** focuses on notebook generation only. For execution, PDF, or HTML features, 
see the [migration guide](https://github.com/QuantEcon/sphinx-tojupyter/blob/main/MIGRATION.md).
```

```{contents} Options
---
depth: 1
local: 
---
```

## tojupyter_conversion_mode

Specifies which writer to use when constructing notebooks.

| Option | Description |
|--------|-------------|
| `"all"` (default) | Compile complete notebooks which include markdown cells and code blocks |
| `"code"` | Compile notebooks that only contain the code blocks |

`conf.py` usage:

```python
tojupyter_conversion_mode = "all"
```

## tojupyter_static_file_path

Specify paths to static files/folders to copy to the output directory.

`conf.py` usage:

```python
tojupyter_static_file_path = ["source/_static"]
```

## tojupyter_default_lang

Specify default language for code blocks when language is not specified.

`conf.py` usage:

```python
tojupyter_default_lang = "python3"
```

## tojupyter_lang_synonyms

Specify language synonyms.

This is used when parsing code blocks. For example, `python` and `ipython`
have slightly different highlighting directives but contain code that can both be executed on
the same kernel.

`conf.py` usage:

```python
tojupyter_lang_synonyms = ["pycon", "ipython"]
```

## tojupyter_kernels

Specify kernel information for the jupyter notebook metadata.

This is used by Jupyter to connect the correct language kernel and is **required** in `conf.py`.

`conf.py` usage:

```python
tojupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
            },
        "file_extension": ".py",
    },
}
```

## tojupyter_drop_solutions

Drop code blocks that include `:class: solution`.

Useful for generating student versions of notebooks without solutions.

| Values |
|--------|
| `True` (default) |
| `False` |

`conf.py` usage:

```python
tojupyter_drop_solutions = True
```

## tojupyter_drop_tests

Drop code blocks that include `:class: test`.

Useful for removing testing/validation code from user-facing notebooks.

| Values |
|--------|
| `True` (default) |
| `False` |

`conf.py` usage:

```python
tojupyter_drop_tests = True
```

## tojupyter_drop_raw_html

Drop raw HTML/script blocks (e.g., Thebe configuration).

Prevents web-specific content from appearing as markdown cells in notebooks.

| Values |
|--------|
| `True` (default) |
| `False` |

`conf.py` usage:

```python
tojupyter_drop_raw_html = True
```

## tojupyter_images_markdown

Use markdown syntax for images instead of HTML `<img>` tags.

| Values |
|--------|
| `True` (default) |
| `False` |

`conf.py` usage:

```python
tojupyter_images_markdown = True
```

When constructing notebooks this option can be enabled to ignore :class: no-execute
for code-blocks. This is useful for including code examples that may not execute correctly.

`conf.py` usage:

```python
jupyter_ignore_no_execute = True
```

## jupyter_ignore_skip_test

When constructing notebooks this option can be enabled to ignore :class: skip-test
for code-blocks.







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

`conf.py` usage:

```python
jupyter_ignore_skip_test = True
```

## jupyter_allow_html_only

Enable this option to allow `.. only:: html` pass through to the notebooks.







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

`conf.py` usage:

```python
jupyter_allow_html_only = True
```

## jupyter_images_markdown

Force the inclusion of images as native markdown







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

```{note}
when this option is enabled the :scale: option is not supported
in RST.
```

`conf.py` usage:

```python
jupyter_images_markdown = True
```

## jupyter_dependencies

Specify file or directory level dependencies

`conf.py` usage:

```python
jupyter_dependencies = {
    <dir> : ['file1', 'file2'],
    {<dir>}/<file.rst> : ['file1']
}
```

this allows you to specify a companion data file for
a given `RST` document and it will get copied through sphinx
to the `_build` folder.

