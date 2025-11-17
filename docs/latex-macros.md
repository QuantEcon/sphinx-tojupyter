# LaTeX Macros Support

sphinx-tojupyter now supports adding custom LaTeX macros to generated Jupyter notebooks, enabling custom mathematical commands to render correctly.

## Problem

When using custom LaTeX commands in Sphinx documentation (like `\ZZ` for integers, `\RR` for reals), these don't render in Jupyter notebooks because the macro definitions aren't included.

## Solution

Configure `tojupyter_latex_macros` in your `conf.py` to automatically add macro definitions to all generated notebooks.

## Configuration

Add your LaTeX macros to `conf.py`:

```python
# conf.py

# LaTeX macros for Jupyter notebooks
tojupyter_latex_macros = r"""
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\NN}{\mathbb{N}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\CC}{\mathbb{C}}
\newcommand{\EE}{\mathbb{E}}
\newcommand{\PP}{\mathbb{P}}
"""
```

## How It Works

sphinx-tojupyter automatically:

1. Creates a markdown cell at the beginning of each notebook
2. Wraps your macros in `$$...$$` so MathJax processes them
3. Makes the macros available throughout the notebook

The generated notebook will have a cell like:

```markdown
$$
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\NN}{\mathbb{N}}
...
$$
```

## Usage

After configuration, use your custom commands anywhere in your documentation:

```markdown
The set of integers is denoted by $\ZZ$.

The expected value is $\EE[X]$.

$$
\begin{align}
\ZZ &\subset \QQ \subset \RR \subset \CC \\
\NN &\subset \ZZ
\end{align}
$$
```

These will render correctly in both HTML and Jupyter notebook outputs.

## Integration with Sphinx LaTeX

You can reuse your existing Sphinx LaTeX preamble:

```python
# conf.py

# For LaTeX/PDF output
latex_elements = {
    'preamble': r'''
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\NN}{\mathbb{N}}
    ''',
}

# For Jupyter notebooks
# Reuse the same definitions
tojupyter_latex_macros = latex_elements['preamble']
```

## Benefits

- ✅ Custom LaTeX commands work in Jupyter notebooks
- ✅ Consistent rendering across HTML, PDF, and notebook outputs
- ✅ No manual editing of generated notebooks required
- ✅ Works with JupyterLab, Jupyter Notebook, and nbviewer

## Notes

- Macros are added as a visible markdown cell (you can hide it in Jupyter if desired)
- MathJax in Jupyter must be configured to process the macros (default behavior)
- Works with both `\newcommand` and `\def` style definitions

## Example

See the [test suite](../../tests/latex_macros/) for a complete working example.

## Related

- [Issue #58](https://github.com/QuantEcon/sphinx-tojupyter/issues/58)
- [MathJax Documentation](https://docs.mathjax.org/en/latest/input/tex/macros.html)
