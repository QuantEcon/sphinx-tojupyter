------

jupytext:jupytext:

  text_representation:  text_representation:

    extension: .md    extension: .md

    format_name: myst    format_name: myst

kernelspec:kernelspec:

  display_name: Python 3  display_name: Python 3

  language: python  language: python

  name: python3  name: python3

------



(config_example)=(config_example)=

# Example conf.py File# Example conf.py file



A minimal configuration example for sphinx-tojupyter v1.0.After running a sphinx-quickstart you can add the jupyter options needed

for your project in a similar fashion to what is shown belows.

## Minimal Configuration

The below configuration settings are the default ones provided by the

The simplest `conf.py` for notebook generation:[jupinx quickstart tool](https://jupinx.readthedocs.io/en/latest/quickstart.html)



```python```{code-cell} python

# conf.py# Configuration file for the Jupinx documentation builder.

#

project = 'My Project'# This file only contains a selection of the most common options. For a full

author = 'Author Name'# list see the documentation:

# http://www.sphinx-doc.org/en/master/config

# Add sphinx-tojupyter extension

extensions = [# -- Path setup --------------------------------------------------------------

    'sphinx_tojupyter',

]# If extensions (or modules to document with autodoc) are in another directory,

# add these directories to sys.path here. If the directory is relative to the

# Optional: Specify default kernel# documentation root, use os.path.abspath to make it absolute, like shown here.

jupyter_default_kernel = 'python3'#

```# import os

# import sys

Run with:# sys.path.insert(0, os.path.abspath('.'))

```bash

sphinx-build -b jupyter source output

```# -- Project information -----------------------------------------------------



---project = 'DEMO'

copyright = '2019, AUTHOR'

## Complete Exampleauthor = 'AUTHOR'



A more comprehensive configuration with common options:# The short X.Y version

version = '0.1'

```python

# Configuration file for Sphinx documentation using sphinx-tojupyter# The full version, including alpha/beta/rc tags

#release = '0.1'

# For the full list of configuration options see:

# https://sphinx-tojupyter.readthedocs.io/

# -- General configuration ---------------------------------------------------

# -- Path setup --------------------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be

import os# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom

import sys# ones.

extensions = [

# -- Project information -----------------------------------------------------    'sphinx_tojupyter',

    'sphinxcontrib.bibtex',

project = 'My Project']

copyright = '2024, Author Name'

author = 'Author Name'# Add any paths that contain templates here, relative to this directory.

version = '1.0'templates_path = ['templates']

release = '1.0.0'

# The suffix(es) of source filenames.

# -- General Sphinx configuration -------------------------------------------# You can specify multiple suffix as a list of string:

#

extensions = [# source_suffix = ['.rst', '.md']

    'sphinx_tojupyter',      # Notebook generationsource_suffix = '.rst'

    'myst_nb',                # MyST-NB support (optional)

    'myst_parser',            # MyST markdown support (optional)# The master toctree document.

    'sphinx_proof',           # Math theorems/proofs (optional)master_doc = 'index'

]

# List of patterns, relative to source directory, that match files and

# Source files# directories to ignore when looking for source files.

source_suffix = {# This pattern also affects html_static_path and html_extra_path.

    '.rst': 'restructuredtext',exclude_patterns = []

    '.md': 'markdown',

}

# -- Options for HTML output -------------------------------------------------

master_doc = 'index'

# The theme to use for HTML and HTML Help pages.  See the documentation for

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']# a list of builtin themes.

#

# -- HTML output options -----------------------------------------------------html_theme = 'alabaster'



html_theme = 'alabaster'# Add any paths that contain custom static files (such as style sheets) here,

html_static_path = ['_static']# relative to this directory. They are copied after the builtin static files,

# so a file named "default.css" will overwrite the builtin "default.css".

# -- sphinx-tojupyter configuration ------------------------------------------html_static_path = ['static']



# Kernel specifications for different languages

jupyter_kernels = {# -- Extension configuration -------------------------------------------------

    'python3': {

        'kernelspec': {# -- jupyter build configuration ---------------------------------------------------

            'display_name': 'Python 3',jupyter_kernels = {

            'language': 'python',    'python3': {

            'name': 'python3'        'kernelspec': {

        },            'display_name': 'Python',

        'file_extension': '.py'            'language': 'python3',

    },            'name': 'python3'

    'julia': {        },

        'kernelspec': {        'file_extension': '.py'

            'display_name': 'Julia',    },

            'language': 'julia',    'python2': {

            'name': 'julia'        'kernelspec': {

        },            'display_name': 'Python',

        'file_extension': '.jl'            'language': 'python2',

    }            'name': 'python2'

}        },

        'file_extension': '.py'

# Default kernel for notebooks    },

jupyter_default_kernel = 'python3'    'julia-1.1': {

        'kernelspec': {

# Conversion mode: "all" or "code"            'display_name': 'Julia 1.1',

# "all" = convert both code and text            'language': 'julia',

# "code" = convert code blocks only            'name': 'julia-1.1'

jupyter_conversion_mode = "all"        },

        'file_extension': '.jl'

# Write notebook metadata    }

jupyter_write_metadata = True}



# Header code cells to add at the start of each notebook# --------------------------------------------

jupyter_headers = {# jupyter Sphinx Extension conversion settings

    "python3": [# --------------------------------------------

        "# Setup code",

        "import numpy as np",# Conversion Mode Settings

        "import matplotlib.pyplot as plt"# If "all", convert codes and texts into notebook

    ],# If "code", convert codes only

}jupyter_conversion_mode = "all"



# Static file paths for images and assetsjupyter_write_metadata = False

jupyter_static_file_path = ["_static"]

# Location for _static folder

# Language synonyms (e.g., treat "ipython" as "python")jupyter_static_file_path = ["source/_static"]

jupyter_lang_synonyms = ["ipython"]

# Configure jupyter headers

# Allow HTML passthrough in notebooksjupyter_headers = {

jupyter_allow_html_only = True    "python3": [

        # nbformat.v4.new_code_cell("%autosave 0")      #@mmcky please make this an option

# Default language for code blocks without specified language        ],

jupyter_default_lang = "python3"    "julia": [

        ],

# Drop code blocks that are only for HTML output}

jupyter_drop_code = []

# Filename for the file containing the welcome block

# Drop specific tests or patternsjupyter_welcome_block = ""

jupyter_drop_tests = []

#Adjust links to target html (rather than ipynb)

# Dependency resolution for Jupyter directivejupyter_target_html = False

jupyter_dependency_lists = {}

#path to download notebooks from

# Theme-specific CSS for notebooksjupyter_download_nb_urlpath = None

jupyter_theme = "light"

#allow downloading of notebooks

# Additional options for advanced usagejupyter_download_nb = False

jupyter_options = {

    'ignore_no_execute': True,#Use urlprefix images

    'timeout': 60,jupyter_download_nb_image_urlpath = None

}

```#Allow ipython as a language synonym for blocks to be ipython highlighted

jupyter_lang_synonyms = ["ipython"]

---

#Execute skip-test code blocks for rendering of website (this will need to be ignored in coverage testing)

## MyST Markdown Supportjupyter_ignore_skip_test = True



If using MyST markdown files, add `myst_parser` configuration:#allow execution of notebooks

jupyter_execute_notebooks = False

```python

extensions = [# Location of template folder for coverage reports

    'sphinx_tojupyter',jupyter_template_coverage_file_path = False

    'myst_parser',

]# generate html from IPYNB files

jupyter_generate_html = False

myst_enable_extensions = [

    "colon_fence",      # ::: directive syntax# html template specific to your website needs

    "deflist",          # Definition listsjupyter_html_template = ""

    "substitution",     # Text substitutions

]# latex template specific to your website needs

jupyter_latex_template = ""

myst_heading_anchors = 3  # Auto-generate anchors for headers

```#make website

jupyter_make_site = False

---

#force markdown image inclusion

## MyST-NB Glue Supportjupyter_images_markdown = True



For MyST-NB glue functionality:#This is set true by default to pass html to the notebooks

jupyter_allow_html_only=True

```python```

extensions = [

    'sphinx_tojupyter',
    'myst_nb',
]

# MyST-NB settings
nb_execution_mode = "off"  # Don't execute during Sphinx build
```

See {doc}`myst-nb` for complete glue documentation.

---

## LaTeX Macros

For consistent LaTeX macros across HTML and notebooks:

```python
# Define macros once
latex_macros = r"""
    \newcommand{\EE}{\mathbb{E}}
    \newcommand{\PP}{\mathbb{P}}
    \newcommand{\RR}{\mathbb{R}}
"""

# For HTML (MathJax 3)
mathjax3_config = {
    'tex': {
        'macros': {
            'EE': r'\mathbb{E}',
            'PP': r'\mathbb{P}',
            'RR': r'\mathbb{R}',
        }
    }
}

# For notebooks (via sphinx-tojupyter)
jupyter_latex_macros = latex_macros
```

See {doc}`latex-macros` for complete guide.

---

## sphinx-proof Support

For mathematical theorem environments:

```python
extensions = [
    'sphinx_tojupyter',
    'sphinx_proof',
]

# Enable numfig for automatic numbering
numfig = True
```

See [sphinx-proof documentation](https://sphinx-proof.readthedocs.io/) for directive usage.

---

## Common Patterns

### Multi-Language Project

```python
jupyter_kernels = {
    'python3': {...},
    'julia': {...},
    'r': {
        'kernelspec': {
            'display_name': 'R',
            'language': 'r',
            'name': 'ir'
        },
        'file_extension': '.r'
    }
}

# Specify different default kernel
jupyter_default_kernel = 'julia'
```

### Minimal Metadata

For cleaner notebooks, minimize metadata:

```python
jupyter_write_metadata = False  # Don't write extra metadata
jupyter_headers = {}             # No header cells
```

### Custom Static File Locations

```python
jupyter_static_file_path = [
    "_static",
    "images",
    "assets"
]
```

---

## Migration from v0.6.0

If upgrading from v0.6.0, remove these obsolete options:

```python
# ❌ REMOVED - Do not use these:
# jupyter_execute_notebooks = ...
# jupyter_make_site = ...
# jupyter_generate_html = ...
# jupyter_target_html = ...
# jupyter_target_pdf = ...
# jupyter_html_template = ...
# jupyter_latex_template = ...
# jupyter_download_nb = ...
# jupyter_download_nb_urlpath = ...
# jupyter_coverage_dir = ...
```

See {doc}`../MIGRATION` for complete migration guide.

---

## Validation

After configuration, validate with:

```bash
# Test notebook generation
sphinx-build -b jupyter source output

# Check for warnings
sphinx-build -b jupyter source output -W

# Verbose output
sphinx-build -b jupyter source output -v
```

---

## Additional Resources

- {doc}`config-sphinx` - Sphinx-specific configuration
- {doc}`config-extension` - Extension configuration reference
- {doc}`config-extension-notebooks` - Notebook-specific options
- {doc}`builders` - Available builders
- {doc}`../MIGRATION` - Migration from v0.6.0

---

## Minimal Example Repository

A complete minimal example is available:
[sphinx-tojupyter.minimal](https://github.com/QuantEcon/sphinx-tojupyter.minimal)

This includes:
- Basic project structure
- Example `conf.py`
- Sample RST/MyST files
- Generated notebooks
