# Configuration file for testing LaTeX macros support

import sys
import os

# Add sphinx-tojupyter to path
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'LaTeX Macros Test'
author = 'Test Author'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_tojupyter',
]

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
    },
}

# LaTeX macros using standard Sphinx mathjax3_config (RECOMMENDED)
# This works for both HTML and Jupyter notebook outputs
mathjax3_config = {
    'tex': {
        'macros': {
            'ZZ': r'\mathbb{Z}',
            'RR': r'\mathbb{R}',
            'NN': r'\mathbb{N}',
            'QQ': r'\mathbb{Q}',
            'CC': r'\mathbb{C}',
        }
    }
}

# Alternative: Raw LaTeX format (LEGACY)
# Uncomment to test fallback behavior
# tojupyter_latex_macros = r"""
# \newcommand{\ZZ}{\mathbb{Z}}
# \newcommand{\RR}{\mathbb{R}}
# \newcommand{\NN}{\mathbb{N}}
# \newcommand{\QQ}{\mathbb{Q}}
# \newcommand{\CC}{\mathbb{C}}
# """

# Build settings
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
