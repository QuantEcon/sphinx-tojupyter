# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] - 2024-11-19

### 🎉 First Stable Release

Version 1.0 is the first stable release of sphinx-tojupyter, **focused solely on converting 
RST and MyST source files to high-quality Jupyter notebooks**. PDF generation, HTML website 
building, and notebook execution have been removed in favor of seamless integration with 
[Jupyter Book](https://jupyterbook.org/).

See [MIGRATION.md](MIGRATION.md) for upgrade instructions from v0.6.0.

### ❌ Removed Features

**PDF Generation:**
- Removed `jupyterpdf` builder (949 lines removed)
- Removed `make_pdf.py` and related functionality
- Removed configuration options:
  - `jupyter_target_pdf` / `tojupyter_target_pdf`
  - All PDF-specific formatting logic

**HTML Website Generation:**
- Removed `make_site.py` and HTML template generation
- Removed configuration options:
  - `jupyter_target_html` / `tojupyter_target_html`
  - `tojuyter_drop_html_raw`
  - `jupyter_make_site`
  - `jupyter_generate_html`
  - `jupyter_html_template`

**Notebook Execution:**
- Removed `execute_nb.py` and execution infrastructure
- Removed configuration options:
  - `jupyter_execute_notebooks`
  - `jupyter_cache_execute`
  - `jupyter_cache`
  - `jupyter_execution_timeout`
  - `jupyter_allow_errors`
  - `jupyter_execute_kwargs`

**Coverage & Testing:**
- Removed coverage tracking functionality
- Removed configuration options:
  - `jupyter_template_coverage_file_path`
  - `jupyter_coverage_dir`
  - `jupyter_number_workers`

**Dependencies:**
- Removed from `install_requires`: `dask[distributed]`, `nbdime`
- Moved testing tools to development dependencies

### ✨ Enhanced Features

**Core Notebook Generation:**
- Simplified translator logic (220 lines removed from `full.py`, 15% reduction)
- Always use Markdown-style formatting (no PDF/HTML conditionals)
- Cleaner reference handling (68% code reduction in `depart_reference`)
- Flattened package structure (`translators/` package)

**MyST-NB Glue Support:** (Already in v0.6.0, retained)
- Full support for `{glue:text}` and `{glue:figure}` directives
- Cross-document gluing
- Figure captions and formatting

**sphinx-proof Support:** (Already in v0.6.0, retained)
- All 15 directive types supported
- Automatic numbering
- Cross-references

**LaTeX Macros:** (Already in v0.6.0, retained)
- Single configuration for HTML and notebooks
- Standard Sphinx/Jupyter Book approach
- Automatic injection into notebook metadata

### 🏗️ Architecture Changes

**Restructured Codebase:**
- Flattened structure: `sphinx_tojupyter/` → `translators/`
- Removed: `builders/jupyterpdf.py`, `writers/execute_nb.py`, `writers/make_pdf.py`, `writers/make_site.py`
- Renamed: `writers/` → `translators/`
- Simplified: `builders/jupyter.py` (307 → 126 lines, 59% reduction)

**Configuration Simplification:**
- Reduced from 47 to 14 core configuration options (70% reduction)
- Removed all PDF/HTML/execution-related options
- Cleaner, more focused configuration surface

### 📚 Documentation

**New:**
- `MIGRATION.md` - Comprehensive migration guide from v1.x to v2.0
- Enhanced `tests/README.md` - Complete test suite documentation
- Added `latex_macros` to test suite with dedicated session

**Updated:**
- `README.md` - v2.0 focus statement and simplified feature list
- `docs/index.md` - Updated for v2.0, added migration notice
- `docs/config-extension.md` - Simplified to notebooks-only
- `docs/config-extension-notebooks.md` - Focused on v2.0 configs

**Removed:**
- `docs/config-extension-pdf.md`
- `docs/config-extension-html.md`
- `docs/config-extension-execution.md`
- `docs/config-extension-coverage.md`
- `docs/config-extension-exercise.md`

### ✅ Testing & Validation

**Test Infrastructure:**
- Added `latex_macros` to test suite
- All tests pass with zero output changes (backward compatible)
- Comprehensive validation across 6 Python/Sphinx combinations:
  - Python 3.11, 3.12, 3.13
  - Sphinx 7.4, 8.2

**Validation Results:**
- ✅ 100% test pass rate
- ✅ Zero notebook output differences (nbdime validation)
- ✅ Backward compatible with existing notebooks

### 🔄 Migration Path

**For v1.x users:**
1. Review removed features (PDF, HTML, execution)
2. Migrate to Jupyter Book for removed features
3. Update `conf.py` to remove unsupported options
4. See [MIGRATION.md](MIGRATION.md) for detailed instructions

**For new users:**
- ✅ Use sphinx-tojupyter v2.0 for notebook generation
- ✅ Use Jupyter Book for execution, PDF, and HTML

### 🙏 Credits

Major refactoring work by [@mmcky](https://github.com/mmcky) with support from 
[QuantEcon](https://www.quantecon.org).

## [0.6.0] - 2024-11-18

### Added
- **sphinx-proof Support**: Full support for sphinx-proof directives in generated notebooks
  - All 15 directive types: theorem, axiom, lemma, definition, remark, conjecture, corollary, algorithm, criterion, example, property, observation, proposition, assumption, notation, proof
  - Automatic numbering from Sphinx's numfig system
  - Support for titled and untitled directives
  - Support for `:nonumber:` option
  - Clean markdown formatting with bold headers
  - Cross-reference handling
  - Added visitor/depart methods for all sphinx-proof node types
  - Helper methods: `_get_proof_node_number()`, `_format_proof_title()`, `_remove_title_node()`
  - Comprehensive test suite in `tests/sphinx_proof/`
  - Works with existing QuantEcon lecture repositories

### Changed
- **Testing Infrastructure**: Complete overhaul to use nox for automated testing
  - Matrix testing: Python 3.11, 3.12, 3.13 × Sphinx 7.4, 8.2
  - Full test suite with all optional dependencies
  - Specific test sessions for sphinx-proof and MyST-NB glue
  - Cross-platform testing (Ubuntu, macOS, Windows)
  - Added `noxfile.py` with 24 test sessions
  - Updated `.github/workflows/ci.yml` (formerly tests.yml) with consolidated CI/CD pipeline
  - Removed old conda-based workflow
  - Added comprehensive `TESTING.md` documentation
  
- **Python & Sphinx Requirements**: Updated minimum versions
  - Python: Now requires >=3.11 (dropped 3.9, 3.10)
  - Sphinx: Now requires >=7.0 (dropped 5.x, 6.x)
  - Updated `setup.py` with `python_requires` and `extras_require` for testing

- **Code Modernization**:
  - Replaced deprecated `distutils` with `shutil` equivalents
  - Updated to use `importlib.metadata` instead of `pkg_resources`
  - Removed Python 2 compatibility code
  - Fixed raw string literals for proper escaping

### Fixed
- **Documentation Build**: Fixed Sphinx 8.x compatibility issues
  - Set `language = 'en'` instead of None in `docs/conf.py`
  - Created missing `docs/_static/` directory
  - Fixed syntax errors and malformed links in documentation
  - Converted non-executable code blocks to plain code blocks
  - Fixed cross-reference warnings
  
- **Build Artifacts**: Cleaned up version control
  - Removed `docs/_build/` from git tracking (185 files)
  - Removed `tests/sphinx_proof/_build/` from git tracking (11 files)
  - Updated `.gitignore` to use `tests/**/_build/` pattern

- **Test Session Python Version**: Fixed `tests-full` nox session
  - Removed hardcoded Python 3.11 requirement
  - Now uses current Python from CI matrix

## [0.5.0] - 2025-11-18

### Added
- **LaTeX Macros Support**: Custom LaTeX commands now work in Jupyter notebooks
  - **Primary**: Uses standard `mathjax3_config` (single source of truth for HTML and notebooks)
  - **Fallback**: Supports `tojupyter_latex_macros` for raw LaTeX format
  - Automatically converts macro definitions to notebook format
  - Enables custom commands like `\ZZ`, `\RR`, `\NN` to render correctly
  - Supports macros with arguments (e.g., `\vec{x}`, `\norm{x}`)
  - Macros added as markdown cell at beginning of each notebook
  - Works seamlessly with existing Jupyter Book projects
  - Compatible with both dict format (`mathjax3_config`) and raw LaTeX (`tojupyter_latex_macros`)
  - Documentation in `docs/latex-macros.md`
  - Test suite in `tests/latex_macros/`
  - Fixes [Issue #58](https://github.com/QuantEcon/sphinx-tojupyter/issues/58)

## [0.4.0] - 2025-11-14

### Added
- **MyST-NB Glue Support**: Full support for MyST-NB's glue functionality
  - Text and number glue with format specifications (e.g., `{glue:text}`var:.2f``)
  - Figure glue for matplotlib plots (e.g., `{glue:figure}my_plot`)
  - **Base64 Image Embedding**: Glued figures are now embedded as base64 data URIs by default, creating truly standalone notebooks that are easy to distribute
  - **Configurable Image URLs**: Optional `tojupyter_glue_urlpath` and `tojupyter_glue_images_urlpath` settings to reference images from web URLs instead of embedding
  - **Automatic Image Copying**: When using URL paths, glued images are automatically copied to `_build/jupyter/glue/` for easy CDN deployment
  - Inline glue references within paragraphs
  - Graceful handling of cross-document glue references
  - Added `visit_inline()` and `depart_inline()` methods to `JupyterTranslator`
  - Added `visit_PendingGlueReference()` and `depart_PendingGlueReference()` methods
  - Added `_image_to_base64()` helper method for image embedding
  - Added `_copy_glued_image()` helper method for URL-based workflows
  - Comprehensive test suite in `tests/glue/`

### Changed
- None

### Fixed
- None

### Known Limitations
- Cross-document glue references (`{glue:text}`other_doc::key``) are not fully resolved by the jupyter builder (MyST-NB limitation)
