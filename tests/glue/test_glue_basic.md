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

# Basic Glue Test

This notebook tests basic MyST-NB glue functionality with sphinx-tojupyter.

## Gluing Values

First, we'll glue some values in a code cell:

```{code-cell} ipython3
from myst_nb import glue

# Glue various types of data
glue("my_variable", "Hello World")
glue("my_number", 3.14159)
glue("my_formatted", 2.71828)
glue("my_integer", 42)
```

## Pasting Glued Values

Now we can reference these glued values in our markdown:

### Text Glue

Simple text value: {glue:text}`my_variable`

### Number Glue

Pi value: {glue:text}`my_number`

Integer value: {glue:text}`my_integer`

### Formatted Number Glue

Formatted to 2 decimal places: {glue:text}`my_formatted:.2f`

Scientific notation: {glue:text}`my_number:.2e`

## Inline Glue

We can also use glue inline with text. For example, the value of pi is approximately {glue:text}`my_number:.4f`, which is often rounded to {glue:text}`my_number:.2f`.

The answer to life, the universe, and everything is {glue:text}`my_integer`.

## Summary

This test demonstrates:
- Gluing string, float, and integer values
- Using `{glue:text}` role to paste values
- Formatting numbers with format specifications
- Inline glue references within paragraphs
