# Test Suite Review - sphinx-tojupyter v2.0

## Current Test Structure

### 1. Base Tests (`tests/base/`)
**Purpose**: Core RST to Jupyter notebook conversion functionality  
**Configuration**: `conf.py` with all v2.0 relevant settings  
**Test Files**: 30+ RST documents testing individual features

#### Tested Features:
- ✅ **code_blocks.rst** - Various code block directives (`.. code::`, `::`, `.. code-block::`)
- ✅ **code_synonyms.rst** - Language synonyms (ipython, pycon, python)
- ✅ **collapse.rst** - Collapsible content directives
- ✅ **dependency.rst** - Document dependencies
- ✅ **download.rst** - Download links
- ✅ **equation_labels.rst** - Labeled equations with :eq: references
- ✅ **footnotes.rst** - Footnote references and definitions
- ✅ **ignore.rst** - Content exclusion
- ✅ **images.rst** - Image handling (local, relative paths)
- ✅ **inline.rst** - Inline code and formatting
- ✅ **jupyter.rst** - Jupyter-specific directives
- ✅ **links.rst** - Internal and external links
- ✅ **links_target.rst** - Link targets and anchors
- ✅ **lists.rst** - Bullet lists, enumerated lists, definition lists
- ✅ **literal_include.rst** - Including external code files
- ✅ **math.rst** - Inline and display math, equation references
- ✅ **notes.rst** - Note/admonition directives
- ✅ **only.rst** - Conditional content (only directive)
- ✅ **quote.rst** - Block quotes
- ✅ **simple_notebook.rst** - Basic notebook structure
- ✅ **slides.rst** - Slide-related features
- ✅ **solutions.rst** - Solution blocks (with tojupyter_drop_solutions)
- ✅ **syntax.rst** - Various RST syntax elements
- ✅ **tables.rst** - Table formatting
- ✅ **tests.rst** - Test blocks (with tojupyter_drop_tests)

**Validation Method**: 
- `check_diffs.py` compares generated notebooks in `_build/jupyter/` against reference notebooks in `ipynb/`
- Uses `nbdime` for semantic notebook diffing (ignores metadata, cell IDs)

### 2. Glue Tests (`tests/glue/`)
**Purpose**: MyST-NB glue functionality (storing/referencing notebook variables)  
**Format**: Markdown (MyST)  
**Dependencies**: myst-parser, myst-nb

#### Test Coverage:
- ✅ **test_glue_basic.md** - Text and number glue with format specs
- ✅ **test_glue_figures.md** - Matplotlib figure glue
- ✅ **test_glue_cross_doc.md** - Cross-document references (expected warnings)
- ✅ **data_source.md** - Source of glued variables

**Status**: All passing (3 expected warnings for cross-doc refs)

### 3. Sphinx-Proof Tests (`tests/sphinx_proof/`)
**Purpose**: Mathematical theorem/proof directive support  
**Format**: Markdown (MyST)  
**Dependencies**: myst-parser, sphinx-proof

#### Test Coverage:
- ✅ **test_basic_directives.md** - Theorem, lemma, definition, etc.
- ✅ **test_numbered_directives.md** - Numbered directives
- ✅ **test_proofs.md** - Proof environments

**Status**: All passing

### 4. LaTeX Macros Tests (`tests/latex_macros/`)
**Purpose**: Custom LaTeX macro support  
**Format**: Markdown (MyST)  
**Configuration**: Both MathJax 2 and MathJax 3 configs

#### Test Coverage:
- ✅ **test_macros.md** - Custom LaTeX commands in notebooks

**Status**: Not run in standard test suite (needs investigation)

### 5. Project Tests (`tests/project/`)
**Purpose**: Full project integration test  
**Format**: Jupyter Book project structure  
**Dependencies**: jupyter-book

**Status**: Requires jupyter-book, may need review for v2.0 compatibility

---

## Test Execution

### Current Nox Sessions:

1. **`nox -s tests`** (default)
   - Tests: base/ only
   - Python: 3.11, 3.12, 3.13
   - Sphinx: 7.4, 8.2
   - Quick validation (~1-2 min)

2. **`nox -s tests-full`**
   - Tests: base/, glue/, sphinx_proof/
   - Python: Current interpreter
   - All dependencies installed
   - Comprehensive validation (~3-5 min)

3. **`nox -s test-glue`**
   - Tests: glue/ only
   - Quick glue feature check

4. **`nox -s test-proof`**
   - Tests: sphinx_proof/ only
   - Quick proof feature check

5. **`nox -s lint`**
   - Flake8 checks
   - Import validation

---

## Gap Analysis

### ✅ Well Covered:
- RST syntax conversion
- Code blocks and language handling
- Math/equations with labels
- Links and references
- Images
- Lists and tables
- Solutions/tests (drop functionality)

### ⚠️ Needs Review:
1. **LaTeX Macros** - Not in standard test run
2. **Project Tests** - Requires jupyter-book, may be deprecated for v2.0
3. **Reference validation** - After removing PDF/HTML logic, are all link types tested?
4. **Markdown (MyST) RST mix** - Do we test mixed format projects?

### ❓ Potentially Missing:
1. **Error handling tests**
   - Invalid syntax
   - Broken references
   - Missing files
   
2. **Edge cases**
   - Empty notebooks
   - Very large notebooks
   - Special characters in filenames
   - Unicode content
   
3. **Configuration tests**
   - All tojupyter_* config options
   - Invalid configurations
   - Kernel specifications
   
4. **Metadata tests**
   - Cell metadata preservation
   - Notebook metadata
   
5. **Multi-language tests**
   - Julia code blocks
   - R code blocks
   - Other kernels

---

## Recommendations

### Priority 1 (Before v2.0 Release):
1. ✅ Verify base tests pass with v2.0 changes (DONE)
2. ✅ Verify glue tests pass (DONE)
3. ✅ Verify sphinx-proof tests pass (DONE)
4. 🔲 Add latex_macros to standard test suite
5. 🔲 Review/update project tests or remove if deprecated
6. 🔲 Add test for internal link types (in-page, cross-doc, with anchors)
7. 🔲 Add test for special characters in links/anchors (parentheses, etc.)

### Priority 2 (Post v2.0):
1. 🔲 Add error handling tests
2. 🔲 Add edge case tests
3. 🔲 Add configuration validation tests
4. 🔲 Increase test coverage metrics
5. 🔲 Add performance benchmarks

### Priority 3 (Future):
1. 🔲 Integration tests with real-world projects
2. 🔲 Regression test suite
3. 🔲 Automated visual diff checking

---

## Test Maintenance

### Reference Notebooks:
- Located in `*/ipynb/` directories
- Should be manually reviewed when features change
- Currently maintained by running build and copying "good" output

### Updating References:
```bash
# After verifying build is correct:
cd tests/base
rm -rf ipynb/
cp -r _build/jupyter/ ipynb/
# Commit updated references
```

### Adding New Tests:
1. Add .rst/.md file to appropriate test directory
2. Add to index file
3. Run build
4. Verify output manually
5. Copy to ipynb/ as reference
6. Run `check_diffs.py` to validate

---

## Questions for Review:

1. **Should we drop project tests?** (requires jupyter-book, may be out of scope for v2.0)
2. **Should latex_macros be in standard suite?** (currently standalone)
3. **Do we need explicit tests for the removed features?** (PDF/HTML/book_index logic)
4. **Should we add CI matrix testing?** (currently just nox sessions)
5. **What's the minimum test coverage we want?** (lines, branches, features)

