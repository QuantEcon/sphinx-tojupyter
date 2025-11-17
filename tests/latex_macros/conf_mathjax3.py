# Configuration file for testing LaTeX macros with mathjax3_config

import sys
import os

# Add sphinx-tojupyter to path
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'LaTeX Macros Test (mathjax3_config)'
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

# LaTeX macros using standard Sphinx mathjax3_config
# This is the RECOMMENDED approach - works for both HTML and notebooks
mathjax3_config = {
    'tex': {
        'macros': {
            'ZZ': r'\mathbb{Z}',
            'RR': r'\mathbb{R}',
            'NN': r'\mathbb{N}',
            'QQ': r'\mathbb{Q}',
            'CC': r'\mathbb{C}',
            'EE': r'\mathbb{E}',
            'PP': r'\mathbb{P}',
            # Macros with arguments
            'vec': [r'\mathbf{#1}', 1],
            'norm': [r'\left\|#1\right\|', 1],
        }
    }
}

# Build settings
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
