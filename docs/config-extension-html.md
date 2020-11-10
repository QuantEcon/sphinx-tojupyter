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

# Converting Notebooks to HTML

```{contents} Options
---
depth: 1
local: 
---
```

## jupyter_generate_html

Enable sphinx to generate HTML versions of notebooks







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

`conf.py` usage:

```{code-cell} python
jupyter_generate_html = True
```

## jupyter_html_template

Specify path to nbconvert html template file

```{note}
Documentation on nbconvert templates can be found
[here](https://nbconvert.readthedocs.io/en/latest/customizing.html#Customizing-nbconvert)
```

`conf.py` usage:

```{code-cell} python
jupyter_html_template = "theme/template/<file>.tpl"
```

## jupyter_make_site

Enable sphinx to construct a complete website

```{todo}
## Todo

Document all the extra elements this option does over jupyter_generate_html

```

This option:

1. fetches coverage statistics if [coverage](coverage_extension_coverage) is enabled.

`conf.py` usage:

```{code-cell} python
jupyter_make_site = True
```

## jupyter_download_nb

Request Sphinx to generate a collection of download notebooks to support a website

`conf.py` usage:

```{code-cell} python
jupyter_download_nb = True
```

## jupyter_download_nb_images_urlpath

Apply a url prefix when writing images in Jupyter notebooks for download notebook set.

`conf.py` usage:

```{code-cell} python
jupyter_images_urlpath = "s3://<path>/_static/img/"
```

## jupyter_theme

Specify theme name

`conf.py` usage:

```{code-cell} python
jupyter_theme = <theme-name>
```

The theme should be located in the path of jupyter_theme_path. The default
path would be: `theme/<theme-name>/`

## jupyter_theme_path

Specify location for theme files





|Value|
|:--------------------------------------------------------------------------------------------------:|
|"theme" (|**|default|**|)|

`conf.py` usage:

```{code-cell} python
jupyter_theme_path = "theme"
```

## jupyter_template_path

Specify path for templates





|Value|
|:--------------------------------------------------------------------------------------------------:|
|"templates" (|**|default|**|)|

`conf.py` usage:

```{code-cell} python
jupyter_template_path = "templates"
```

## jupyter_template_html

Specify `html` template to be used by `nbconvert`

`conf.py` usage:

```{code-cell} python
jupyter_template_html = <path to tpl file>
```

The template file should be located in the path of `jupyter_template_path`.
The default path would be: `templates/<tpl file>`

