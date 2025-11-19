# URL Path Test Suite

This test suite verifies that the `tojupyter_urlpath` and `tojupyter_image_urlpath` configuration options work correctly when generating Jupyter notebooks.

## Purpose

Test that:
1. **Cross-document links** are prefixed with the configured base URL
2. **In-page anchors** remain as local `#anchor` references
3. **External links** are not modified

## Configuration

The test uses these settings in `conf.py`:

```python
tojupyter_urlpath = "https://continuous-time-mcs.quantecon.org/"
tojupyter_image_urlpath = "https://continuous-time-mcs.quantecon.org/_static/"
```

## Test Files

- `index.rst` - Main index with toctree
- `doc_a.rst` - Document with cross-document links to doc_b and in-page anchors
- `doc_b.rst` - Document with cross-document links to doc_a and in-page anchors

## Running Tests

```bash
cd tests/urlpath
make jupyter
```

## Verification

After building, check the generated notebooks in `_build/jupyter/`:

### Expected Results

**Cross-document links (should have base URL):**
- `doc_b.ipynb` → `https://continuous-time-mcs.quantecon.org/doc_b.ipynb`
- `doc_b.ipynb#section` → `https://continuous-time-mcs.quantecon.org/doc_b.ipynb#section`

**In-page anchors (should remain local):**
- `#section-1` → `#section-1`
- `#exercise-1` → `#exercise-1`

**External links (should not be modified):**
- `https://quantecon.org` → `https://quantecon.org`
- `https://www.python.org/` → `https://www.python.org/`

## Manual Verification

Open the generated notebooks and search for these patterns:

```bash
# Check for properly prefixed cross-document links
grep -r "https://continuous-time-mcs.quantecon.org/doc_[ab].ipynb" _build/jupyter/

# Check that in-page anchors remain local
grep -r "](#doc-[ab]-" _build/jupyter/

# Check that external links are preserved
grep -r "https://quantecon.org" _build/jupyter/
grep -r "https://www.sphinx-doc.org/" _build/jupyter/
```

## Test Cases

### doc_a.rst tests:
1. `:doc:`doc_b`` → prefixed URL
2. `:ref:`doc-b-section-2`` (cross-doc) → prefixed URL with anchor
3. `:ref:`doc-a-section-1`` (in-page) → local anchor
4. External link to quantecon.org → unchanged

### doc_b.rst tests:
1. `:doc:`doc_a`` → prefixed URL
2. `:ref:`doc-a-section-2`` (cross-doc) → prefixed URL with anchor
3. `:ref:`doc-b-section-1`` (in-page) → local anchor
4. Mixed list with cross-doc, in-page, and external links

## Automated Testing

This test can be run via nox:

```bash
nox -s test-urlpath
```

The test will:
1. Build the notebooks
2. Parse the generated JSON
3. Verify link patterns match expected behavior
4. Report any discrepancies
