# Configuration file for testing MyST-NB glue support

import sys
import os

# Add sphinx-tojupyter to path
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'Glue Test'
author = 'Test Author'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_nb',
    'sphinx_tojupyter',
]

# MyST-NB configuration
# Execute notebooks during build to generate glue data
nb_execution_mode = "cache"
nb_execution_timeout = 60

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
]

# Jupyter notebook configuration
jupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

jupyter_conversion_mode = "all"
jupyter_write_metadata = True
jupyter_static_file_path = []
jupyter_download_nb = False
jupyter_target_html = False
jupyter_target_pdf = False
jupyter_images_markdown = True
jupyter_theme = "light"
jupyter_allow_html_only = False

# Exclude patterns - exclude jupyter_execute to prevent recursion and ipynb to avoid duplicate processing
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints', 'jupyter_execute', 'ipynb', '**.ipynb', 'README.md']

# HTML theme (needed for build even though we're generating notebooks)
html_theme = 'alabaster'
