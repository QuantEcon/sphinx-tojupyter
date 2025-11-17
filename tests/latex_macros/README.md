# LaTeX Macros Test Suite

Test suite for LaTeX macro support in sphinx-tojupyter.

## Quick Start

```bash
# Build notebooks
sphinx-build -b jupyter . ipynb

# Check that macros were added
cat ipynb/test_macros.ipynb | python -m json.tool | head -30
```

## Configuration

The `conf.py` file defines LaTeX macros using:

```python
tojupyter_latex_macros = r"""
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\NN}{\mathbb{N}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\CC}{\mathbb{C}}
"""
```

## Expected Result

The generated notebook should have:
1. A hidden markdown cell at the beginning with the LaTeX macro definitions
2. All custom commands (`\ZZ`, `\RR`, etc.) rendering properly when opened in Jupyter

## Verification

Open the generated notebook in Jupyter and verify that:
- $\ZZ$ renders as ℤ (blackboard bold Z)
- $\RR$ renders as ℝ (blackboard bold R)  
- $\NN$ renders as ℕ (blackboard bold N)
- And so on...

## See Also

- [Issue #58](https://github.com/QuantEcon/sphinx-tojupyter/issues/58)
- [Jupyter MathJax Documentation](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Typesetting%20Equations.html)
