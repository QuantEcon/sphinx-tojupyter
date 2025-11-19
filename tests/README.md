# Testing sphinx-tojupyter

This directory contains comprehensive tests for the sphinx-tojupyter extension.

## Test Suites

### 1. Base Tests (`base/`)
Core RST to Jupyter notebook conversion functionality.
- **Format:** reStructuredText (RST)
- **Tests:** 26 RST documents covering all core features
- **Validation:** Compared against reference notebooks in `base/ipynb/`
- **Run:** `nox -s tests` or `make jupyter` from `base/`

### 2. Glue Tests (`glue/`)
MyST-NB glue functionality (storing and referencing notebook variables).
- **Format:** Markdown (MyST)
- **Dependencies:** myst-parser, myst-nb
- **Tests:** Text glue, figure glue, cross-document references
- **Run:** `nox -s test-glue` or `make jupyter` from `glue/`

### 3. Sphinx-Proof Tests (`sphinx_proof/`)
Mathematical theorem and proof directive support.
- **Format:** Markdown (MyST)
- **Dependencies:** myst-parser, sphinx-proof
- **Tests:** Theorem, lemma, definition, proof environments
- **Run:** `nox -s test-proof` or `make jupyter` from `sphinx_proof/`

### 4. LaTeX Macros Tests (`latex_macros/`)
Custom LaTeX macro support in math expressions.
- **Format:** Markdown (MyST)
- **Tests:** Custom LaTeX commands, MathJax configuration
- **Run:** `make jupyter` from `latex_macros/`

### 5. Configuration Validation Tests (`test_config_validation.py`)
Tests for v2.0 configuration handling and backward compatibility.
- **Format:** pytest-based unit tests
- **Tests:** 
  - Deprecated config options handled gracefully
  - Core v2.0 config options work correctly
  - Minimal configuration works
- **Run:** `nox -s test-config`

### 6. Project Tests (`project/`)
Full project integration test with Jupyter Book.
- **Format:** Jupyter Book project structure
- **Dependencies:** jupyter-book
- **Status:** May be deprecated in v2.0 (out of scope)

## Running Tests

### Quick Test (Base Only)
```bash
nox -s "tests-3.13(sphinx='8.2')"
```

### Full Test Matrix (All Python/Sphinx combinations)
```bash
nox -s tests
```

### Comprehensive Suite (Base + Glue + Proof)
```bash
nox -s tests-full
```

### Individual Test Suites
```bash
nox -s test-glue    # MyST-NB glue tests
nox -s test-proof   # sphinx-proof tests
nox -s test-config  # Configuration validation tests
```

## Test Validation

Tests are validated using `check_diffs.py` which:
- Compares generated notebooks against reference notebooks
- Uses `nbdime` for semantic diffing (ignores metadata, cell IDs)
- Fails if content differs

## Updating Reference Notebooks

After making changes that affect output (intentionally):

```bash
cd tests/base
# Run build
make jupyter
# Review differences
git diff ipynb/
# If correct, commit updated references
git add ipynb/
git commit -m "test: update reference notebooks for <reason>"
```

## Test Coverage

- ✅ RST syntax conversion
- ✅ Code blocks (multiple languages)
- ✅ Math (inline, display, labeled equations)
- ✅ Links (internal, external, anchors)
- ✅ Images and figures
- ✅ Lists (bullet, enumerated, definition)
- ✅ Tables
- ✅ Footnotes and citations
- ✅ MyST-NB glue (text, figures, cross-doc)
- ✅ Sphinx-proof (theorem, lemma, proof)
- ✅ LaTeX macros
- ✅ Solutions/tests (drop functionality)
- ✅ Configuration validation (v2.0)
- ✅ Deprecated options backward compatibility

## Development

### Adding New Tests
1. Create test file in appropriate directory
2. Add to index/toctree
3. Run `make jupyter`
4. Verify output manually
5. Copy to `ipynb/` as reference
6. Run `check_diffs.py` to validate

### Test Requirements
- Python 3.11, 3.12, or 3.13
- Sphinx 7.4+ or 8.2+
- Optional: myst-parser, myst-nb, sphinx-proof (for full suite)