#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test configuration for tojupyter_drop_raw_html

import sphinx
SPHINX_VERSION = sphinx.version_info

# -- General configuration ------------------------------------------------

extensions = ['sphinx_tojupyter']

templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

# General information about the project.
project = 'Raw HTML Drop Test'
copyright = '2025, QuantEcon'
author = 'QuantEcon'

version = '1.0'
release = '1.0'

language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = False

# -- Jupyter notebook options -----------------------------------------------

# Kernel specs
jupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

# Notebook generation options
jupyter_options = {
    'conversion_mode': 'all',
}

# Drop raw HTML by default (Thebe config, script tags, etc.)
tojupyter_drop_raw_html = True  # This is the default

# Standard config values
tojupyter_kernels = jupyter_kernels
tojupyter_conversion_mode = jupyter_options['conversion_mode']
tojupyter_default_lang = "python3"
tojupyter_static_file_path = []
tojupyter_images_markdown = True

# -- HTML output options ---------------------------------------------------

html_theme = 'alabaster'
html_static_path = []
htmlhelp_basename = 'raw_html_test_doc'
