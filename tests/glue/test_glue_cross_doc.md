---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Cross-Document Glue Test

This notebook tests MyST-NB cross-document glue references.

## Referencing Values from Another Document

We can reference values glued in `data_source.md`:

The shared value is: {glue:text}`data_source::shared_value`

The shared number is: {glue:text}`data_source::shared_number:.2f`

## Referencing Figures from Another Document

Here's the shared plot from the data source document:

```{glue:figure} data_source::shared_plot
:name: fig-shared
:alt: Shared plot from data source

This figure was glued in data_source.md and referenced here.
```

## Summary

This test demonstrates cross-document glue references, which allow:

- Referencing glued text values from other documents
- Referencing glued figures from other documents
- Using format specifications with cross-document references
