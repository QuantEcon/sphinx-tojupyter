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

# Data Source for Cross-Document Glue

This document provides glued data that can be referenced from other documents.

```{code-cell} ipython3
from myst_nb import glue
import matplotlib.pyplot as plt
import numpy as np

# Glue some values for cross-document reference
glue("shared_value", "This is shared across documents")
glue("shared_number", 123.456)

# Create a shared figure
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax.set_title('Shared Plot')
glue("shared_plot", fig, display=False)
```

These values are glued and can be referenced from other documents using the syntax:

- `{glue:text}`data_source.md::shared_value``
- `{glue:text}`data_source.md::shared_number``
- `{glue}`data_source.md::shared_plot``
