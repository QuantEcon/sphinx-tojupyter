# Migration Guide: v0.6.0 to v1.0.0

## Overview

Version 1.0.0 is the **first stable release** that focuses `sphinx-tojupyter` on its core strength: 
converting RST and MyST source files to Jupyter notebooks.

**What Changed:**
- ❌ **Removed:** PDF generation (use [Jupyter Book](https://jupyterbook.org/))
- ❌ **Removed:** HTML website generation (use [Jupyter Book](https://jupyterbook.org/))
- ❌ **Removed:** Notebook execution (use [Jupyter Book](https://jupyterbook.org/) or [myst-nb](https://myst-nb.readthedocs.io/))
- ❌ **Removed:** Coverage tracking
- ❌ **Removed:** Exercise/solution management
- ✅ **Enhanced:** MyST-NB glue support
- ✅ **Enhanced:** sphinx-proof directive support
- ✅ **Enhanced:** LaTeX macro support

**Rationale:** Jupyter Book and MyST-NB provide excellent execution, PDF generation, and 
website building capabilities. Version 1.0 delegates these features to focus on producing 
high-quality notebooks from documentation source.

## Breaking Changes

### Removed Configuration Options

The following `conf.py` options are **no longer supported**:

#### PDF-Related Options (Removed)
```python
# ❌ No longer supported
jupyter_target_pdf = False
tojupyter_target_pdf = False
```

**Migration:** Use Jupyter Book for PDF generation:
```bash
jupyter-book build --builder pdflatex yourbook/
```

#### HTML-Related Options (Removed)
```python
# ❌ No longer supported
jupyter_target_html = False
tojupyter_target_html = False
tojuyter_drop_html_raw = True
jupyter_make_site = False
jupyter_generate_html = False
jupyter_html_template = "basic.tpl"
```

**Migration:** Use Jupyter Book for HTML generation:
```bash
jupyter-book build yourbook/
```

#### Execution-Related Options (Removed)
```python
# ❌ No longer supported
jupyter_execute_notebooks = False
jupyter_cache_execute = False
jupyter_cache = "."
jupyter_execution_timeout = 30
jupyter_allow_errors = False
jupyter_execute_kwargs = {}
```

**Migration:** Use Jupyter Book or myst-nb for execution:

**conf.py** for Jupyter Book:
```python
extensions = ["jupyter_book"]

# Execution settings
nb_execution_mode = "cache"  # or "auto", "force", "off"
nb_execution_timeout = 30
nb_execution_allow_errors = False
```

#### Coverage-Related Options (Removed)
```python
# ❌ No longer supported
jupyter_template_coverage_file_path = False
jupyter_drop_tests = False
jupyter_coverage_dir = "executed"
jupyter_number_workers = 1
```

**Migration:** Use [nbval](https://github.com/computationalmodelling/nbval) or 
[pytest-notebook](https://pytest-notebook.readthedocs.io/) for notebook testing.

### Removed Builders

The following Sphinx builders are **no longer available**:

```bash
# ❌ No longer supported
make jupyterpdf
```

**Migration:** Use Jupyter Book:
```bash
jupyter-book build --builder pdflatex yourbook/
```

### Retained Configuration Options

The following core notebook generation options **remain supported** (with renamed prefix):

```python
# ✅ Supported in v1.0 (note: jupyter_* → tojupyter_*)
extensions = ["sphinx_tojupyter"]

tojupyter_conversion_mode = "all"  # or "code"
tojupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

tojupyter_default_lang = "python3"
tojupyter_lang_synonyms = ["pycon", "ipython"]

tojupyter_static_file_path = ["source/_static"]
tojupyter_dependency_lists = {}

tojupyter_drop_solutions = True
tojupyter_drop_tests = True
tojupyter_drop_raw_html = True  # NEW in v1.0
tojupyter_images_markdown = True
```

### Configuration Option Renames

All configuration options have been renamed from `jupyter_*` to `tojupyter_*`:

| Old (v0.6) | New (v1.0) | Status |
|------------|------------|--------|
| `jupyter_conversion_mode` | `tojupyter_conversion_mode` | ✅ Renamed |
| `jupyter_kernels` | `tojupyter_kernels` | ✅ Renamed |
| `jupyter_default_lang` | `tojupyter_default_lang` | ✅ Renamed |
| `jupyter_lang_synonyms` | `tojupyter_lang_synonyms` | ✅ Renamed |
| `jupyter_static_file_path` | `tojupyter_static_file_path` | ✅ Renamed |
| `jupyter_drop_solutions` | `tojupyter_drop_solutions` | ✅ Renamed |
| `jupyter_drop_tests` | `tojupyter_drop_tests` | ✅ Renamed |
| `jupyter_images_markdown` | `tojupyter_images_markdown` | ✅ Renamed |
| `jupyter_dependencies` | `tojupyter_dependency_lists` | ✅ Renamed |
| `jupyter_header_block` | (removed) | ❌ Deleted |
| `jupyter_write_metadata` | (removed) | ❌ Deleted |
| `jupyter_allow_html_only` | (removed) | ❌ Deleted |

## Migration Strategies

### Strategy 1: Continue Using v1.x

If you need PDF generation or execution features:

```bash
# Stay on v1.x
pip install 'sphinx-tojupyter<2.0'
```

### Strategy 2: Migrate to Jupyter Book

**Recommended for most users.** Jupyter Book provides a complete publishing workflow:

1. **Install Jupyter Book:**
   ```bash
   pip install jupyter-book
   ```

2. **Create a Jupyter Book structure:**
   ```bash
   jupyter-book create mybook/
   ```

3. **Use sphinx-tojupyter v1.0 for notebook generation:**
   ```python
   # conf.py
   extensions = ["sphinx_tojupyter"]
   
   jupyter_kernels = {
       "python3": {
           "kernelspec": {
               "display_name": "Python",
               "language": "python3",
               "name": "python3"
           },
           "file_extension": ".py",
       }
   }
   ```

4. **Generate notebooks:**
   ```bash
   make jupyter
   ```

5. **Build with Jupyter Book:**
   ```bash
   jupyter-book build mybook/
   ```

### Strategy 3: Hybrid Approach

Use sphinx-tojupyter v1.0 for notebook generation, then use specialized tools:

- **Execution:** [myst-nb](https://myst-nb.readthedocs.io/) or [papermill](https://papermill.readthedocs.io/)
- **PDF:** [nbconvert](https://nbconvert.readthedocs.io/) or Jupyter Book
- **HTML:** [nbconvert](https://nbconvert.readthedocs.io/) or Jupyter Book

## Feature Equivalents

### Execution

**v1.x:**
```python
jupyter_execute_notebooks = True
jupyter_cache_execute = True
```

**v1.0 + Jupyter Book:**
```python
extensions = ["jupyter_book"]
nb_execution_mode = "cache"
```

### PDF Generation

**v1.x:**
```bash
make jupyterpdf
```

**v1.0 + Jupyter Book:**
```bash
jupyter-book build --builder pdflatex mybook/
```

### HTML Website

**v1.x:**
```python
jupyter_make_site = True
jupyter_generate_html = True
```

**v1.0 + Jupyter Book:**
```bash
jupyter-book build mybook/
```

### MyST-NB Glue (Enhanced in v1.0)

**v1.0 has full support:**

```markdown
\```{code-cell} ipython3
from myst_nb import glue
glue("my_variable", 42)
\```

The answer is {glue:text}`my_variable`.
```

### sphinx-proof (Enhanced in v1.0)

**v1.0 has full support:**

```markdown
\```{prf:theorem} Pythagorean Theorem
In a right triangle: $a^2 + b^2 = c^2$
\```
```

## Support

For questions or issues during migration:

- **Issues:** [GitHub Issues](https://github.com/QuantEcon/sphinx-tojupyter/issues)
- **Documentation:** [Read the Docs](https://sphinx-tojupyter.readthedocs.io/)
- **QuantEcon:** [contact@quantecon.org](mailto:contact@quantecon.org)

## Version History

- **v1.0.0** (2024) - Focus on notebook generation, remove PDF/HTML/execution
- **v1.0.0** (2023) - Stable release with all features
- **v0.6.0** and earlier - Development releases
