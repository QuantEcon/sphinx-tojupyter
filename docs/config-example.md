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

# Optional: Specify default language
tojupyter_default_lang = 'python3'
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
tojupyter_kernels = {
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

# Default language for code blocks
tojupyter_default_lang = 'python3'

# Conversion mode: "all" (markdown+code) or "code" (code only)
tojupyter_conversion_mode = "all"

# Static file paths for images and assets
tojupyter_static_file_path = ["_static"]

# Language synonyms (e.g., treat "ipython" as "python")
tojupyter_lang_synonyms = ["ipython"]

# Use markdown syntax for images (vs HTML)
tojupyter_images_markdown = True

# Drop raw HTML/script blocks (Thebe config, etc.)
tojupyter_drop_raw_html = True
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
# For HTML and notebooks (MathJax 3)
mathjax3_config = {
    'tex': {
        'macros': {
            'EE': r'\mathbb{E}',
            'PP': r'\mathbb{P}',
            'RR': r'\mathbb{R}',
        }
    }
}

# Macros are automatically injected into notebooks

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

See the [MIGRATION.md](https://github.com/QuantEcon/sphinx-tojupyter/blob/main/MIGRATION.md) guide for complete migration instructions.

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
