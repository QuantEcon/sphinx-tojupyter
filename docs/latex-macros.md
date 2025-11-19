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

# LaTeX Macros Support

sphinx-tojupyter automatically adds custom LaTeX macros to generated Jupyter notebooks, enabling custom mathematical commands to render correctly.

## Problem

When using custom LaTeX commands in Sphinx documentation (like `\ZZ` for integers, `\RR` for reals), these don't render in Jupyter notebooks because the macro definitions aren't included.

## Solution

Define your macros once using Sphinx's standard `mathjax3_config`, and they'll automatically work in both HTML and Jupyter notebook outputs.

## Configuration

### Option 1: Using `mathjax3_config` (Recommended)

This is the **standard Sphinx/Jupyter Book approach** and the recommended method:

```python
# conf.py

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
        }
    }
}
```

**Benefits:**
- ✅ Single source of truth for both HTML and notebooks
- ✅ Standard Sphinx configuration
- ✅ Works with existing Jupyter Book projects
- ✅ No duplicate configuration needed

### Option 2: Using `tojupyter_latex_macros` (Alternative)

For raw LaTeX format or when you need more control:

```python
# conf.py

# LaTeX macros for Jupyter notebooks
tojupyter_latex_macros = r"""
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\NN}{\mathbb{N}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\CC}{\mathbb{C}}
"""
```

**Note:** If both are configured, `mathjax3_config` takes priority.

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

## Advanced: Macros with Arguments

You can define macros that take arguments:

```python
# conf.py

mathjax3_config = {
    'tex': {
        'macros': {
            'vec': [r'\mathbf{#1}', 1],      # \vec{x} -> \mathbf{x}
            'norm': [r'\left\|#1\right\|', 1],  # \norm{x} -> \left\|x\right\|
            'abs': [r'\left|#1\right|', 1],     # \abs{x} -> \left|x\right|
        }
    }
}
```

The array format is `[definition, num_args]`.

## Integration with Jupyter Book

If you're using Jupyter Book with `_config.yml`, the configuration works the same way:

```yaml
# _config.yml

sphinx:
  config:
    mathjax3_config:
      tex:
        macros:
          "ZZ": "\\mathbb{Z}"
          "RR": "\\mathbb{R}"
          "NN": "\\mathbb{N}"
          "argmax": "arg\\,max"
          "argmin": "arg\\,min"
```

**No additional configuration needed!** Your macros will automatically work in generated notebooks.

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

See the test suite in `tests/latex_macros/` for a complete working example.

## Related

- [Issue #58](https://github.com/QuantEcon/sphinx-tojupyter/issues/58)
- [MathJax Documentation](https://docs.mathjax.org/en/latest/input/tex/macros.html)
