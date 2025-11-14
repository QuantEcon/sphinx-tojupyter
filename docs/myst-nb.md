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

# MyST-NB Integration

`sphinx-tojupyter` supports [MyST-NB](https://myst-nb.readthedocs.io/) markdown syntax, including the powerful **glue** functionality for storing and referencing notebook variables.

## Setup

To use MyST-NB features with sphinx-tojupyter, add both extensions to your `conf.py`:

```python
extensions = [
    'myst_nb',
    'sphinx_tojupyter',
]

# Configure MyST-NB execution
nb_execution_mode = "cache"  # or "auto" or "force"
nb_execution_timeout = 60
```

## Glue Functionality

Glue allows you to store variables, numbers, and figures in code cells and reference them later in markdown text.

### Basic Text Glue

Store and reference text values:

````markdown
```python
from myst_nb import glue

my_variable = "Hello World"
glue("greeting", my_variable)
```

The stored value is: {glue:text}`greeting`
````

Output: "The stored value is: Hello World"

### Number Glue with Formatting

Store numbers and format them on reference:

````markdown
```python
from myst_nb import glue

pi = 3.14159265359
glue("pi_value", pi)
```

- Pi value: {glue:text}`pi_value`
- Formatted to 2 decimals: {glue:text}`pi_value:.2f`
- Scientific notation: {glue:text}`pi_value:.2e`
````

### Figure Glue

Store and embed matplotlib figures:

````markdown
```python
import matplotlib.pyplot as plt
import numpy as np
from myst_nb import glue

# Create a plot
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 2 * np.pi, 100)
ax.plot(x, np.sin(x))
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')

# Glue the figure (display=False to avoid showing it twice)
glue("sine_plot", fig, display=False)
```

Now reference the figure:

\```{glue:figure} sine_plot
:name: fig-sine
:alt: Sine wave plot

A sine wave plotted over the interval [0, 2π].
\```

You can reference the figure like this: {ref}`fig-sine`
````

### Inline Glue References

Glue works seamlessly within paragraphs:

````markdown
```python
from myst_nb import glue

result = 42
accuracy = 0.95
glue("answer", result)
glue("accuracy", accuracy)
```

The computation yielded {glue:text}`answer` with an accuracy 
of {glue:text}`accuracy:.1%`.
````

Output: "The computation yielded 42 with an accuracy of 95.0%."

## Supported Features

✅ **Fully Supported:**
- Text and string glue
- Number glue with Python format specifications
- Figure glue (matplotlib, plotly, etc.)
- Inline glue references within paragraphs
- Figure captions and labels
- Math expressions (via nodes.math_block)

⚠️ **Known Limitations:**
- Cross-document glue references (`{glue:text}`other_doc::key``) show warnings when using the jupyter builder (MyST-NB limitation)
- Cross-document references insert empty placeholders but don't crash

## How It Works

MyST-NB processes `{glue:}` directives and creates standard docutils nodes:
- `nodes.inline` with "pasted-text" class for text/numbers
- `nodes.figure` for glued figures
- `nodes.image` for glued images
- `nodes.math_block` for glued math

The `sphinx-tojupyter` translator handles these nodes and embeds the glued content in the generated notebooks.

## Format Specifications

Glue supports Python format specifications for numbers:

| Format | Example | Result |
|--------|---------|--------|
| `.2f` | `{glue:text}`num:.2f`` | 3.14 |
| `.4f` | `{glue:text}`num:.4f`` | 3.1416 |
| `.2e` | `{glue:text}`num:.2e`` | 3.14e+00 |
| `.1%` | `{glue:text}`num:.1%`` | 314.2% |
| `:,` | `{glue:text}`num:,`` | 3,141.59 |

## Testing

The test suite in `tests/glue/` contains working examples:
- `test_glue_basic.md` - Text and number glue examples
- `test_glue_figures.md` - Figure glue examples
- `test_glue_cross_doc.md` - Cross-document reference examples

Run the tests:
```bash
cd tests/glue
make jupyter
```

## Configuration

### Image Embedding for Glued Figures

By default, glued figures are embedded as base64 data URIs directly in the notebook markdown cells, making notebooks truly standalone and easy to distribute. You can configure this behavior:

```python
# conf.py

# Option 1: Use base64 embedding (default - standalone notebooks)
# No configuration needed, this is the default behavior

# Option 2: Reference images from a web URL
tojupyter_glue_urlpath = "https://example.com/images/"
# Images will be referenced as: https://example.com/images/filename.png

# Alternative name for the same option:
tojupyter_glue_images_urlpath = "https://example.com/images/"
```

**Benefits of base64 embedding (default):**
- Notebooks are completely standalone
- No external file dependencies
- Easy to share and distribute
- Works immediately when opened

**When to use URL paths:**
- When notebook file size is a concern
- When images are already hosted on a CDN
- When you want to update images without regenerating notebooks

## Troubleshooting

### Glue values not appearing

**Problem:** Glue references show as empty in notebooks

**Solutions:**
- Ensure `nb_execution_mode` is set to "cache", "auto", or "force" (not "off")
- Check that notebooks executed successfully (look for `.jupyter_cache/` directory)
- Verify glue keys are spelled correctly

### Import errors

**Problem:** `ModuleNotFoundError: No module named 'myst_nb'`

**Solution:**
```bash
pip install myst-nb>=0.14.0
```

### Cross-document warnings

**Problem:** Warnings like "Pending glue reference document not found"

**Explanation:** This is expected behavior. Cross-document glue references are not fully supported by the jupyter builder. The implementation handles this gracefully by inserting empty placeholders.

## See Also

- [MyST-NB Documentation](https://myst-nb.readthedocs.io/)
- [MyST-NB Glue Documentation](https://myst-nb.readthedocs.io/en/latest/render/glue.html)
- [MyST Parser Documentation](https://myst-parser.readthedocs.io/)
