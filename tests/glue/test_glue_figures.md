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

# Glue Figures Test

This notebook tests MyST-NB glue functionality with figures and images.

## Creating and Gluing a Figure

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
from myst_nb import glue

# Create a simple plot
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
ax.plot(x, y)
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
ax.set_title('Sine Wave')
ax.grid(True)

# Glue the figure (display=False to avoid showing it twice)
glue("sine_plot", fig, display=False)

# Create another plot for inline use
fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.bar(['A', 'B', 'C', 'D'], [3, 7, 2, 5])
ax2.set_title('Bar Chart')
glue("bar_chart", fig2, display=False)
```

## Displaying Glued Figures

### Simple Figure Paste

Here's the sine wave plot:

```{glue} sine_plot
```

### Figure with Caption

We can add a caption using the `glue:figure` directive:

```{glue:figure} sine_plot
:name: fig-sine-glue
:alt: Sine wave plot

This is a sine wave plotted over the interval $[0, 2\pi]$.
```

You can reference the figure like this: see {ref}`fig-sine-glue`.

### Another Figure

Here's the bar chart:

```{glue:figure} bar_chart
:name: fig-bar-glue
:figwidth: 600px

A simple bar chart showing four categories.
```

## Summary

This test demonstrates:
- Creating matplotlib figures in code cells
- Gluing figures with `glue()` function
- Using `{glue}` directive for simple figure paste
- Using `{glue:figure}` directive with captions and labels
- Referencing glued figures
