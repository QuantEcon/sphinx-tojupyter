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

(config_example)=
# Example conf.py File

A minimal configuration example for sphinx-tojupyter v1.0.

## Minimal Configuration

The simplest `conf.py` for notebook generation:

```python
# conf.py

project = 'My Project'
author = 'Author Name'

# Add sphinx-tojupyter extension
extensions = [
    'sphinx_tojupyter',
]

# Optional: Specify default kernel
jupyter_default_kernel = 'python3'
```

Run with:
```bash
sphinx-build -b jupyter source output
```

---

## Complete Example

A more comprehensive configuration with common options:

```python
# Configuration file for Sphinx documentation using sphinx-tojupyter
#
# For the full list of configuration options see:
# https://sphinx-tojupyter.readthedocs.io/

# -- Path setup --------------------------------------------------------------

import os
import sys

# -- Project information -----------------------------------------------------

project = 'My Project'
copyright = '2024, Author Name'
author = 'Author Name'
version = '1.0'
release = '1.0.0'

# -- General Sphinx configuration -------------------------------------------

extensions = [
    'sphinx_tojupyter',      # Notebook generation
    'myst_nb',                # MyST-NB support (optional)
    'myst_parser',            # MyST markdown support (optional)
    'sphinx_proof',           # Math theorems/proofs (optional)
]

# Source files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

master_doc = 'index'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- HTML output options -----------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- sphinx-tojupyter configuration ------------------------------------------

# Kernel specifications for different languages
jupyter_kernels = {
    'python3': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'file_extension': '.py'
    },
    'julia': {
        'kernelspec': {
            'display_name': 'Julia',
            'language': 'julia',
            'name': 'julia'
        },
        'file_extension': '.jl'
    }
}

# Default kernel for notebooks
jupyter_default_kernel = 'python3'

# Conversion mode: "all" or "code"
jupyter_conversion_mode = "all"

# Write notebook metadata
jupyter_write_metadata = True

# Header code cells to add at the start of each notebook
jupyter_headers = {
    "python3": [
        "# Setup code",
        "import numpy as np",
        "import matplotlib.pyplot as plt"
    ],
}

# Static file paths for images and assets
jupyter_static_file_path = ["_static"]

# Language synonyms (e.g., treat "ipython" as "python")
jupyter_lang_synonyms = ["ipython"]

# Allow HTML passthrough in notebooks
jupyter_allow_html_only = True
```

---

## MyST Markdown Support

If using MyST markdown files, add `myst_parser` configuration:

```python
extensions = [
    'sphinx_tojupyter',
    'myst_parser',
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
]

myst_heading_anchors = 3
```

---

## MyST-NB Glue Support

For MyST-NB glue functionality:

```python
extensions = [
    'sphinx_tojupyter',
    'myst_nb',
]

nb_execution_mode = "off"
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

# For notebooks
jupyter_latex_macros = latex_macros
```

See {doc}`latex-macros` for complete guide.

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
```

---

## Additional Resources

- {doc}`config-sphinx` - Sphinx-specific configuration
- {doc}`config-extension` - Extension configuration reference
- {doc}`config-extension-notebooks` - Notebook-specific options
- {doc}`builders` - Available builders

---

## Minimal Example Repository

A complete minimal example is available:
[sphinx-tojupyter.minimal](https://github.com/QuantEcon/sphinx-tojupyter.minimal)
