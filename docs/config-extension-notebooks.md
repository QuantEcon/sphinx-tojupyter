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

```{contents} Options
---
depth: 1
local: 
---
```

## jupyter_conversion_mode

Specifies which writer to use when constructing notebooks.













|Option|Description|
|:------------------------------------------------:|:------------------------------------------------:|
|"all" (|**|default|**|)|compile complete notebooks which include |`|markdown cells|`| and |`|code blocks|`|
|"code"|compile notebooks that only contain the |`|code blocks|`|.|

`conf.py` usage:

```python
jupyter_conversion_mode = "all"
```

## jupyter_static_file_path

Specify path to _static folder.

`conf.py` usage:

```python
jupyter_static_file_path = ["source/_static"]
```

## jupyter_header_block

Add a header block to every generated notebook by specifying an RST file

`conf.py` usage:

```python
jupyter_header_block = ["source/welcome.rst"]
```

## jupyter_default_lang

Specify default language for collection of RST files

`conf.py` usage:

```python
jupyter_default_lang = "python3"
```

## jupyter_lang_synonyms

Specify any language synonyms.

This will be used when parsing code blocks. For example, python and ipython
have slightly different highlighting directives but contain code that can both be executed on
the same kernel

`conf.py` usage:

```python
jupyter_lang_synonyms = ["pycon", "ipython"]
```

## jupyter_kernels

Specify kernel information for the jupyter notebook metadata.

This is used by jupyter to connect the correct language kernel and is **required** in `conf.py`.

`conf.py` usage:

```python
jupyter_kernels = {
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

```{todo}
## Todo

See Issue [196](https://github.com/QuantEcon/sphinx-tojupyter/issues/196%29)

```

## jupyter_write_metadata

write time and date information at the top of each notebook as notebook metadata

```{note}
This option is slated to be deprecated
```

## jupyter_options

An dict-type object that is used by dask to control execution

```{todo}
## Todo

This option needs to be reviewed

```

## jupyter_drop_solutions

Drop `code-blocks` that include `:class: solution`







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

```{todo}
## Todo

This option needs to be reviewed

```

## jupyter_drop_tests

Drop `code-blocks` that include ``:class: test`







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

```{todo}
## Todo

This option needs to be reviewed

```

## jupyter_ignore_no_execute:







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

When constructing notebooks this option can be enabled to ignore :class: no-execute
for code-blocks. This is useful for html writer for pages that are meant to fail
but shouldn't be included in coverage tests.

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

## jupyter_target_html

Enable this option to generate notebooks that favour the inclusion of `html`
in notebooks to support more advanced features.







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

Supported Features:

1. html based table support
1. image inclusion as `html` figures

`conf.py` usage:

```python
jupyter_target_html = True
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

