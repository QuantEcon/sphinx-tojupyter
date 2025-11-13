# MyST-NB Glue Test Suite

Tests for MyST-NB glue functionality support in sphinx-tojupyter.

## Quick Start

```bash
# Install dependencies
pip install myst-nb matplotlib

# Run tests
make jupyter

# Clean
make clean
```

## Test Files

- **test_glue_basic.md** - Text/number glue with formatting
- **test_glue_figures.md** - Matplotlib figure glue
- **test_glue_cross_doc.md** - Cross-document references (demonstrates limitation)
- **data_source.md** - Source data for cross-doc tests
- **index.md** - Test suite entry point

## Expected Results

✅ **Working:**
- Text glue: `{glue:text}\`my_var\``
- Formatted numbers: `{glue:text}\`pi:.2f\``
- Figure glue: `{glue:figure}my_plot`
- Inline references within paragraphs

⚠️ **Known Limitation:**
- Cross-document glue shows warnings (MyST-NB limitation with jupyter builder)

## Verification

```bash
make jupyter
grep "Hello World" ipynb/test_glue_basic.ipynb  # Should find glued text
ls ipynb/jupyter_execute/*.png                   # Should see figure images
```

## Implementation

See `sphinx_tojupyter/writers/translate_all.py`:
- `visit_inline()` / `depart_inline()` - Handle glued text
- `visit_PendingGlueReference()` / `depart_PendingGlueReference()` - Handle cross-doc refs

## See Also

- [MyST-NB Glue Docs](https://myst-nb.readthedocs.io/en/latest/render/glue.html)
- [Project CHANGELOG](../../CHANGELOG.md)
- [Main README](../../README.md)
