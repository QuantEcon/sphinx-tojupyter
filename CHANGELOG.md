# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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
