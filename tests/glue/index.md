---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
---

# MyST-NB Glue Tests

This is a test suite for MyST-NB glue support in sphinx-tojupyter.

## Test Files

```{toctree}
:maxdepth: 1

test_glue_basic
test_glue_figures
test_glue_cross_doc
data_source
```

## Purpose

These tests verify that sphinx-tojupyter can properly convert MyST markdown files with glue functionality into Jupyter notebooks.

## What is Glue?

MyST-NB's `glue` feature allows you to:
1. Store variables, figures, and other objects in code cells with `glue(key, value)`
2. Reference those glued values in markdown using roles like `{glue:text}key` or `{glue:figure}key`

When converted to notebooks, the glued values should be resolved and embedded as regular markdown/images.
