# sphinx-tojupyter v2.0 Refactoring Plan

**Goal**: Transform sphinx-tojupyter from a multi-purpose tool into a focused, specialized extension for generating high-quality Jupyter notebooks from RST and MyST source files.

**Strategy**: Clean v1.0 → v2.0 breaking change, removing all execution, HTML generation, and PDF features in favor of Jupyter Book integration.

**Timeline**: Single major PR for complete refactoring

**Primary Users**: QuantEcon team and projects

---

## 🎯 Mission Statement (v2.0)

**sphinx-tojupyter v2.0 does ONE thing exceptionally well:**
Generate high-quality Jupyter notebooks (`.ipynb`) from Sphinx documentation source files (RST & MyST).

**What we DO:**
- ✅ Convert RST/MyST → Jupyter notebooks
- ✅ Support MyST-NB features (glue, etc.)
- ✅ Support sphinx-proof directives
- ✅ Support sphinx-exercise directives
- ✅ Multi-language kernel support
- ✅ LaTeX macro support
- ✅ Custom Jupyter directives

**What we DON'T do (delegate to Jupyter Book/Sphinx):**
- ❌ Execute notebooks (use Jupyter Book)
- ❌ Generate HTML (use Jupyter Book)
- ❌ Generate PDF (use Jupyter Book)
- ❌ Build websites (use Jupyter Book)
- ❌ Manage downloads (use Jupyter Book)

---

## 📊 Expected Impact

| Metric | Before (v1) | After (v2) | Change |
|--------|-------------|------------|--------|
| Config options | ~45 | ~12 | **-73%** |
| Core files | 12 | ~7 | **-42%** |
| Dependencies | 6+ | 3-4 | **-40%** |
| Lines of code | ~3000+ | ~1500 | **-50%** |
| Builders | 2 | 1 | **-50%** |

---

## 🚀 Phase 0: Preparation

**Goal**: Establish v1.0 baseline and set up for refactoring

### Checklist

- [x] **Tag current state as v1.0.0**
  ```bash
  git tag -a v1.0.0 -m "Release v1.0.0 - Final version before v2.0 refactoring"
  git push origin v1.0.0
  ```

- [x] **Create GitHub release for v1.0.0** - Complete with release notes

- [x] **Create v2.0 development branch**
  ```bash
  git checkout -b v2-refactor
  ```

- [x] **Document current feature list** (documented in v1.0.0 release notes)

- [x] **Create backup/archive** of current state - v1.0.0 tag serves as backup

**Exit Criteria**: 
- ✅ v1.0.0 tag exists
- ✅ v1.0.0 GitHub release created
- ✅ v2-refactor branch created and checked out
- ✅ Ready to start breaking changes

**Phase 0 Complete! ✅**

---

## 🧹 Phase 1: Core Cleanup - Remove Obsolete Features

**Goal**: Delete all code related to execution, HTML, PDF, and website generation

### 1.1: Delete Obsolete Files ✅

- [x] **Delete PDF builder**: `sphinx_tojupyter/builders/jupyterpdf.py`
- [x] **Delete execution writer**: `sphinx_tojupyter/writers/execute_nb.py`
- [x] **Delete PDF writer**: `sphinx_tojupyter/writers/make_pdf.py`
- [x] **Delete site builder**: `sphinx_tojupyter/writers/make_site.py`
- [x] **Delete HTML converter**: `sphinx_tojupyter/writers/convert.py`

### 1.2: Clean Up Jupyter Builder

File: `sphinx_tojupyter/builders/jupyter.py`

- [ ] Remove Dask client imports and initialization
- [ ] Remove `ExecuteNotebookWriter` import and usage
- [ ] Remove `MakeSiteWriter` import and usage
- [ ] Remove `convertToHtmlWriter` import and usage
- [ ] Remove execution-related instance variables:
  - `execution_vars`
  - `download_execution_vars`
  - `client`
  - `execution_status_code`
  - `futures`, `futuresInfo`, `dask_log`
  - `threads_per_worker`, `n_workers`
- [ ] Remove execution logic from `init()` method
- [ ] Remove execution logic from `prepare_writing()` method
- [ ] Remove execution logic from `write_doc()` method
- [ ] Remove execution logic from `finish()` method
- [ ] Remove `executedir`, `reportdir`, `errordir` directory handling
- [ ] Remove download directory handling (`downloadsdir`, `downloadsExecutedir`)
- [ ] Simplify builder to focus only on notebook generation

### 1.3: Clean Up Configuration

File: `sphinx_tojupyter/__init__.py`

**Remove these config options (30+ options to delete):**

#### Execution Related
- [ ] Remove `tojupyter_execute_nb`
- [ ] Remove `tojupyter_execute_notebooks`
- [ ] Remove `tojupyter_threads_per_worker`
- [ ] Remove `tojupyter_number_workers`

#### HTML/Website Generation
- [ ] Remove `tojupyter_generate_html`
- [ ] Remove `tojupyter_html_template`
- [ ] Remove `tojupyter_make_site`
- [ ] Remove `tojupyter_target_html`

#### Download Management
- [ ] Remove `tojupyter_download_nb`
- [ ] Remove `tojupyter_download_nb_execute`
- [ ] Remove `tojupyter_download_nb_urlpath`
- [ ] Remove `tojupyter_download_nb_image_urlpath`

#### PDF Related
- [ ] Remove `tojupyter_target_pdf`
- [ ] Remove `tojupyter_latex_template`
- [ ] Remove `tojupyter_latex_template_book`
- [ ] Remove `tojupyter_pdf_logo`
- [ ] Remove `tojupyter_bib_file`
- [ ] Remove `tojupyter_pdf_author`
- [ ] Remove `tojupyter_pdf_showcontentdepth`
- [ ] Remove `tojupyter_pdf_urlpath`
- [ ] Remove `tojupyter_pdf_excludepatterns`
- [ ] Remove `tojupyter_pdf_book`
- [ ] Remove `tojupyter_pdf_book_index`
- [ ] Remove `tojupyter_pdf_book_title`
- [ ] Remove `tojupyter_pdf_book_name`

#### Theme/Template
- [ ] Remove `tojupyter_theme`
- [ ] Remove `tojupyter_theme_path`
- [ ] Remove `tojupyter_template_path`

#### Miscellaneous
- [ ] Remove `tojupyter_dependencies` (if unused)
- [ ] Remove `tojuyter_drop_html_raw` (note: has typo)

#### Builder Registration
- [ ] Remove `app.add_builder(JupyterPDFBuilder)` line
- [ ] Remove import of `JupyterPDFBuilder`

**Keep these essential configs (~12 options):**

- [x] `tojupyter_kernels` - Kernel specifications
- [x] `tojupyter_default_lang` - Default programming language
- [x] `tojupyter_lang_synonyms` - Language name mappings
- [x] `tojupyter_conversion_mode` - 'all' or 'code'
- [x] `tojupyter_drop_solutions` - Drop solution blocks
- [x] `tojupyter_drop_tests` - Drop test blocks
- [x] `tojupyter_static_file_path` - Static files to copy
- [x] `tojupyter_images_markdown` - Use markdown for images
- [x] `tojupyter_urlpath` - Base URL for links
- [x] `tojupyter_image_urlpath` - Base URL for images
- [x] `tojupyter_glue_urlpath` - Base URL for glue images
- [x] `tojupyter_latex_macros` - LaTeX macros for MathJax
- [x] `tojupyter_dependency_lists` - Notebook dependencies
- [x] `tojupyter_nextprev_ignore` - Navigation items to ignore

### 1.4: Update Dependencies

File: `setup.py`

- [ ] Update `VERSION` to `'v2.0.0'`
- [ ] Update `LONG_DESCRIPTION` with v2.0 information
- [ ] Remove `dask[distributed]` from `install_requires`
- [ ] Remove `nbdime` from `install_requires` (if not needed)
- [ ] Remove `nox` from `install_requires` (move to test extras if needed)
- [ ] Review `nbconvert` - keep only if still needed for core functionality
- [ ] Keep: `sphinx>=7.0`, `myst-nb>=0.14`, `pyyaml`, `nbformat`
- [ ] Update classifiers if needed
- [ ] Update description to reflect v2.0 focus

### 1.5: Clean Up Utilities

File: `sphinx_tojupyter/writers/utils.py`

- [ ] Review and remove execution-related utility functions
- [ ] Review and remove HTML-generation utility functions
- [ ] Review and remove PDF-generation utility functions
- [ ] Keep only essential utilities (file copying, dependency management)

**Exit Criteria**: 
- ✅ All obsolete files deleted
- ✅ Builder simplified to notebook generation only
- ✅ Configuration reduced to ~12 essential options
- ✅ Dependencies cleaned up
- ✅ No references to execution/HTML/PDF in core code

---

## 📁 Phase 2: Reorganize Structure

**Goal**: Create cleaner, more intuitive code organization

### 2.1: Reorganize Core Files

- [ ] **Flatten builders**:
  - Move `sphinx_tojupyter/builders/jupyter.py` → `sphinx_tojupyter/builder.py`
  - Delete empty `sphinx_tojupyter/builders/` directory
  - Update imports in `__init__.py`

- [ ] **Rename writer**:
  - Move `sphinx_tojupyter/writers/jupyter.py` → `sphinx_tojupyter/writer.py`
  - Update imports in `builder.py` and `__init__.py`

### 2.2: Create Translators Package

- [ ] **Create new directory**: `sphinx_tojupyter/translators/`
- [ ] **Create `translators/__init__.py`** with exports
- [ ] **Move and rename files**:
  - `writers/translate_all.py` → `translators/full.py`
  - `writers/translate_code.py` → `translators/code.py`
- [ ] **Create `translators/base.py`** (if extracting common logic)
- [ ] **Update imports** in `writer.py`

### 2.3: Reorganize Directives

- [ ] **Keep structure** (already clean):
  - `sphinx_tojupyter/directive/` → keep as-is
  - Or rename to `directives/` (plural) for consistency

### 2.4: Simplify Utils

- [ ] **Keep or merge**: 
  - Option A: Keep `sphinx_tojupyter/utils.py` as simplified standalone
  - Option B: Move relevant utils into appropriate modules
- [ ] **Delete `writers/` directory** if now empty

### 2.5: Update All Imports

- [ ] Update imports in `__init__.py`
- [ ] Update imports in `builder.py`
- [ ] Update imports in `writer.py`
- [ ] Update imports in translators
- [ ] Update imports in directives
- [ ] Search for any other import references: `from sphinx_tojupyter.builders` → `from sphinx_tojupyter`
- [ ] Search for any other import references: `from sphinx_tojupyter.writers` → `from sphinx_tojupyter.translators`

**Exit Criteria**: 
- ✅ Flatter, more intuitive structure
- ✅ All imports updated and working
- ✅ No broken references
- ✅ Code still runs (even if tests need updating)

---

## 📝 Phase 3: Documentation Overhaul

**Goal**: Create clear, focused documentation for v2.0

### 3.1: Create Migration Guide

- [ ] **Create `docs/migration-v2.md`** with:
  - Overview of v2.0 changes
  - Breaking changes list
  - Configuration mapping (old → new)
  - Feature alternatives (execution → Jupyter Book)
  - Complete migration examples
  - How to pin to v1.0.0 if needed

### 3.2: Update Main Documentation

- [ ] **Update `docs/index.md`**:
  - Clear v2.0 mission statement
  - Feature list (what we DO and DON'T do)
  - Quick start example
  - Link to migration guide
  - Updated table of contents

- [ ] **Create `docs/quickstart.md`**:
  - 5-minute quick start guide
  - Minimal working example
  - Basic configuration

- [ ] **Simplify `docs/configuration.md`**:
  - Document only the ~12 core config options
  - Remove all execution/HTML/PDF options
  - Clear examples for each option
  - Best practices

- [ ] **Create `docs/conversion-modes.md`**:
  - Explain 'all' vs 'code' conversion modes
  - Use cases for each mode
  - Examples

- [ ] **Update `docs/directives.md`**:
  - Keep Jupyter directives documentation
  - Ensure examples are clear

- [ ] **Update/Keep `docs/myst-integration.md`**:
  - MyST-NB glue support (just added!)
  - sphinx-proof integration
  - sphinx-exercise integration

- [ ] **Create `docs/jupyter-book.md`**:
  - How to use sphinx-tojupyter with Jupyter Book
  - Complete workflow example
  - Configuration recommendations
  - Execution, HTML, PDF with Jupyter Book

- [ ] **Update `docs/examples.md`**:
  - Update examples to reflect v2.0
  - Remove execution/HTML/PDF examples
  - Add Jupyter Book workflow examples

### 3.3: Remove Obsolete Documentation

- [ ] **Delete or archive**:
  - `docs/config-extension-execution.md`
  - `docs/config-extension-html.md`
  - `docs/config-extension-pdf.md`
  - `docs/config-extension-coverage.md` (if coverage removed)
  - `docs/builders.md` (if it documents multiple builders)

- [ ] **Update remaining docs**:
  - `docs/config-extension.md` - remove obsolete sections
  - `docs/config-project.md` - update for v2.0
  - `docs/config-example.md` - simplify example configuration

### 3.4: Update README

- [ ] **Update `README.md`** with:
  - Clear v2.0 positioning
  - "What's New in v2.0" section
  - Simplified feature list
  - Installation instructions
  - Quick start (3-5 lines)
  - Jupyter Book integration mention
  - Link to migration guide
  - Removed features section
  - Simplified examples

### 3.5: Update CHANGELOG

- [ ] **Update `CHANGELOG.md`** with:
  - v2.0.0 entry with complete breaking changes list
  - v1.0.0 entry noting it as final v1.x release
  - Migration instructions reference

### 3.6: Update Example Configurations

- [ ] **Update `docs/config-example.md`**:
  - Remove all obsolete config options
  - Show clean v2.0 configuration
  - Add comments explaining each option

- [ ] **Update test configurations**:
  - `tests/base/conf.py` - simplify
  - `tests/glue/conf.py` - ensure works with v2.0
  - Other test conf.py files

**Exit Criteria**: 
- ✅ Complete migration guide exists
- ✅ All documentation reflects v2.0 reality
- ✅ No references to removed features (except in migration guide)
- ✅ Clear Jupyter Book integration story
- ✅ README is compelling and accurate

---

## 🧪 Phase 4: Update Tests

**Goal**: Ensure tests reflect v2.0 scope and all pass

### 4.1: Remove Obsolete Tests

- [ ] **Identify and remove**:
  - Execution tests
  - HTML generation tests
  - PDF generation tests
  - Download management tests
  - Website building tests
  - Coverage tests (if coverage removed)
  - Any tests that depend on removed features

### 4.2: Update Core Tests

- [ ] **Review `tests/base/`**:
  - Ensure all tests still relevant
  - Update conf.py for v2.0
  - Fix any broken tests from refactoring
  - Ensure RST → notebook conversion works

- [ ] **Review `tests/glue/`**:
  - Ensure glue tests still pass
  - Update conf.py if needed
  - Verify MyST-NB integration works

- [ ] **Review `tests/sphinx_proof/`**:
  - Ensure sphinx-proof tests still pass
  - Update conf.py if needed
  - Verify directive conversion works

- [ ] **Update test utilities** (`tests/check_diffs.py`, etc.):
  - Remove execution-related utilities
  - Keep notebook comparison utilities

### 4.3: Update Test Documentation

- [ ] **Update `tests/README.md`**:
  - Reflect v2.0 test structure
  - Remove references to obsolete tests
  - Update test running instructions

- [ ] **Update `TESTING.md`** (if exists):
  - Update for v2.0 scope
  - Simplify test suite description

- [ ] **Update `TESTING_QUANTECON.md`** (if relevant):
  - Update for QuantEcon specific usage with v2.0

### 4.4: Add New Tests (if needed)

- [ ] **Integration tests**:
  - Test basic RST → notebook conversion
  - Test basic MyST → notebook conversion
  - Test with minimal configuration
  - Smoke tests for main functionality

- [ ] **Regression tests**:
  - Ensure existing working features still work
  - Test edge cases

### 4.5: Run Complete Test Suite

- [ ] **Run all tests**: `pytest tests/` or `make test`
- [ ] **Fix all failures**
- [ ] **Verify no warnings** (or only expected ones)
- [ ] **Test on clean environment**

**Exit Criteria**: 
- ✅ All tests pass
- ✅ No tests for removed features
- ✅ Core conversion tests work
- ✅ MyST-NB glue tests work
- ✅ sphinx-proof tests work
- ✅ Test documentation updated

---

## 🔖 Phase 5: Version and Release Preparation

**Goal**: Finalize v2.0 for release

### 5.1: Update Version Information

- [ ] **Update `setup.py`**:
  - Ensure `VERSION = 'v2.0.0'`
  - Update `LONG_DESCRIPTION` with v2.0 focus
  - Update `download_url` for v2.0.0 tag
  - Update classifiers if needed

- [ ] **Update `sphinx_tojupyter/__init__.py`**:
  - Ensure version detection works
  - Update any version-specific code

### 5.2: Final CHANGELOG Update

- [ ] **Complete `CHANGELOG.md`** entry for v2.0.0:
  - Add release date
  - Ensure all breaking changes listed
  - Ensure all removals documented
  - Ensure migration guide referenced
  - Add credits/acknowledgments

### 5.3: Final Documentation Review

- [ ] **Proofread all documentation**
- [ ] **Check all internal links work**
- [ ] **Verify code examples are correct**
- [ ] **Ensure migration guide is complete**
- [ ] **Check README is compelling**

### 5.4: Pre-Release Testing

- [ ] **Install in clean environment**: `pip install -e .`
- [ ] **Test basic usage** on sample project
- [ ] **Test with Jupyter Book** workflow
- [ ] **Run full test suite** one more time
- [ ] **Check for any deprecation warnings**
- [ ] **Test documentation builds** (`cd docs && make html`)

### 5.5: Create Release Materials

- [ ] **Write PR description** with:
  - Summary of v2.0 changes
  - Breaking changes highlights
  - Migration instructions
  - Testing done
  - Links to documentation

- [ ] **Prepare release notes** for v2.0.0:
  - User-friendly summary
  - Feature highlights
  - Breaking changes
  - Migration guide link

**Exit Criteria**: 
- ✅ Version is 2.0.0 everywhere
- ✅ CHANGELOG is complete
- ✅ All documentation proofread
- ✅ Pre-release testing successful
- ✅ Release materials prepared

---

## 🚢 Phase 6: Release

**Goal**: Ship v2.0 to users

### 6.1: Final Commit and PR

- [ ] **Commit all changes**:
  ```bash
  git add -A
  git commit -m "Refactor to v2.0 - Focus on notebook generation only"
  ```

- [ ] **Push branch**:
  ```bash
  git push origin v2-refactor
  ```

- [ ] **Create PR** to main:
  ```bash
  gh pr create --title "v2.0 Refactoring - Specialized Notebook Generator" \
    --body "$(cat PR_TEMPLATE.md)"
  ```

### 6.2: Review and Merge

- [ ] **Review PR** (self-review or team review)
- [ ] **Address any feedback**
- [ ] **Ensure CI passes** (if configured)
- [ ] **Merge to main**

### 6.3: Tag and Release

- [ ] **Tag release**:
  ```bash
  git checkout main
  git pull origin main
  git tag -a v2.0.0 -m "Release v2.0.0 - Focused notebook generator"
  git push origin v2.0.0
  ```

- [ ] **Create GitHub release**:
  - Use tag v2.0.0
  - Title: "v2.0.0 - Major Refactoring"
  - Description: Release notes
  - Mark as major release

### 6.4: Publish to PyPI

- [ ] **Build distribution**:
  ```bash
  python setup.py sdist bdist_wheel
  ```

- [ ] **Test upload to TestPyPI** (optional):
  ```bash
  twine upload --repository testpypi dist/*
  ```

- [ ] **Upload to PyPI**:
  ```bash
  twine upload dist/*
  ```

- [ ] **Verify installation**:
  ```bash
  pip install sphinx-tojupyter==2.0.0
  ```

### 6.5: Post-Release

- [ ] **Update documentation site** (if hosted separately)
- [ ] **Announce release**:
  - QuantEcon team notification
  - GitHub discussions/announcements
  - Any relevant community channels
- [ ] **Monitor for issues**
- [ ] **Be ready to do patch release** if critical bugs found

**Exit Criteria**: 
- ✅ v2.0.0 merged to main
- ✅ v2.0.0 tagged and released on GitHub
- ✅ v2.0.0 available on PyPI
- ✅ Documentation updated
- ✅ Release announced

---

## 📋 Working Notes

### Current Status
<!-- Update this as we progress -->
- **Phase**: Phase 0 Complete ✅ - Ready to start Phase 1
- **Last Updated**: 2025-11-19
- **Blockers**: None
- **Next Steps**: Start Phase 1 - Core Cleanup (delete obsolete files)

### Key Decisions Made
<!-- Document important decisions as we go -->
1. v1.0 → v2.0 clean break (no deprecation period)
2. Single PR for entire refactoring
3. Remove all execution/HTML/PDF features
4. Focus solely on notebook generation
5. Delegate advanced features to Jupyter Book

### Issues to Resolve
<!-- Track any issues that come up -->
- [ ] None yet

### Questions for Discussion
<!-- Track any questions that arise -->
- [ ] None yet

---

## 📚 Reference Information

### Files to DELETE
```
sphinx_tojupyter/builders/jupyterpdf.py
sphinx_tojupyter/writers/execute_nb.py
sphinx_tojupyter/writers/make_pdf.py
sphinx_tojupyter/writers/make_site.py
sphinx_tojupyter/writers/convert.py
docs/config-extension-execution.md
docs/config-extension-html.md
docs/config-extension-pdf.md
docs/config-extension-coverage.md
```

### Files to MOVE/RENAME
```
sphinx_tojupyter/builders/jupyter.py → sphinx_tojupyter/builder.py
sphinx_tojupyter/writers/jupyter.py → sphinx_tojupyter/writer.py
sphinx_tojupyter/writers/translate_all.py → sphinx_tojupyter/translators/full.py
sphinx_tojupyter/writers/translate_code.py → sphinx_tojupyter/translators/code.py
```

### Files to CREATE
```
sphinx_tojupyter/translators/__init__.py
sphinx_tojupyter/translators/base.py (optional)
docs/migration-v2.md
docs/quickstart.md
docs/jupyter-book.md
docs/conversion-modes.md
```

### Config Options to REMOVE (30+)
See Phase 1, Section 1.3 for complete list

### Config Options to KEEP (12)
See Phase 1, Section 1.3 for complete list

### Dependencies to REMOVE
- `dask[distributed]`
- `nbdime` (if not needed)
- `nox` from install_requires (move to test extras)

---

## 🎉 Success Criteria

v2.0 is ready when:
- ✅ All obsolete features removed
- ✅ Codebase reduced by ~50%
- ✅ Config options reduced to ~12
- ✅ Dependencies reduced by ~40%
- ✅ All tests pass
- ✅ Documentation is complete and accurate
- ✅ Migration guide is comprehensive
- ✅ Can generate notebooks from RST/MyST sources
- ✅ Works seamlessly with Jupyter Book
- ✅ v2.0.0 released to PyPI
