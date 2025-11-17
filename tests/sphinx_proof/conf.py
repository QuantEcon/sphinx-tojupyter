# Configuration file for sphinx-proof tests
import sys
import os

# -- Project information -----------------------------------------------------
project = 'sphinx-proof Test'
copyright = '2025, QuantEcon'
author = 'QuantEcon'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx_proof',
    'myst_parser',
    'sphinx_tojupyter'
]

# Jupyter configuration
tojupyter_static_file_path = ["source"]
tojupyter_target_html = False
tojupyter_default_lang = "python3"
tojupyter_lang_synonyms = ['ipython']
tojupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

# MyST configuration
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "colon_fence"
]

# Enable numfig for numbered directives
numfig = True
numfig_format = {
    'theorem': 'Theorem %s',
    'axiom': 'Axiom %s',
    'lemma': 'Lemma %s',
    'definition': 'Definition %s',
    'remark': 'Remark %s',
    'conjecture': 'Conjecture %s',
    'corollary': 'Corollary %s',
    'algorithm': 'Algorithm %s',
    'criterion': 'Criterion %s',
    'example': 'Example %s',
    'property': 'Property %s',
    'observation': 'Observation %s',
    'proposition': 'Proposition %s',
    'assumption': 'Assumption %s',
    'notation': 'Notation %s',
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
