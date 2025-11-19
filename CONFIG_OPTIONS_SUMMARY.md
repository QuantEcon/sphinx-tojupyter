# sphinx-tojupyter Configuration Options Summary

**Version:** 1.0 (v1.0-refactor branch)  
**Focus:** RST/MyST to Jupyter Notebook Conversion

## Configuration Options Overview

| Option Name | Type | Default | Status | Description |
|------------|------|---------|--------|-------------|
| **Core Notebook Generation** |
| `tojupyter_kernels` | dict | `JUPYTER_KERNELS` | ✅ Active | Kernel metadata for notebooks (language, display name) |
| `tojupyter_default_lang` | str | `"python3"` | ✅ Active | Default language for code blocks |
| `tojupyter_lang_synonyms` | list | `[]` | ✅ Active | Language synonyms (e.g., "pycon", "ipython" → python) |
| `tojupyter_conversion_mode` | str | `"all"` | ✅ Active | Conversion mode: "all" (markdown+code) or "code" (code only) |
| **Content Control** |
| `tojupyter_drop_solutions` | bool | `True` | ✅ Active | Drop code blocks with `:class: solution` |
| `tojupyter_drop_tests` | bool | `True` | ✅ Active | Drop code blocks with `:class: test` |
| `tojupyter_drop_raw_html` | bool | `True` | ✅ **NEW** | Drop raw HTML/script blocks (Thebe config, etc.) |
| **Asset Handling** |
| `tojupyter_static_file_path` | list | `[]` | ✅ Active | Path(s) to static files to copy |
| `tojupyter_images_markdown` | bool | `True` | ✅ Active | Use markdown syntax for images (vs HTML) |
| **URL Paths** |
| `tojupyter_urlpath` | str/None | `None` | ✅ **FIXED** | Base URL for cross-document links |
| `tojupyter_image_urlpath` | str/None | `None` | ✅ Active | Base URL for image references |
| `tojupyter_glue_urlpath` | str/None | `None` | ✅ Active | Base URL for MyST-NB glue figure references |
| **Advanced** |
| `tojupyter_latex_macros` | str/None | `None` | ✅ Active | Path to LaTeX macros file for math rendering |
| `tojupyter_dependency_lists` | dict | `{}` | ✅ Active | File/directory dependencies to copy |
| `tojupyter_nextprev_ignore` | list | `[]` | ⚠️ Review | List of files to ignore for next/prev navigation |
| **Internal/System** |
| `SPHINX_VERSION` | tuple | (from sphinx) | ✅ Active | Sphinx version information |
| `nb_mime_priority_overrides` | list | `NB_RENDER_PRIORITY` | ✅ Active | MyST-NB MIME type rendering priority |

---

## Status Legend

- ✅ **Active** - Working and tested for notebook generation
- ✅ **NEW** - Recently added in this PR
- ✅ **FIXED** - Fixed in this PR (was broken before)
- ⚠️ **Review** - Needs review/validation for v1.0 focus
- ❌ **Deprecated** - Should be removed
- 🔄 **Changed** - Behavior modified from previous version

---

## Detailed Breakdown

### Core Notebook Generation Options

#### `tojupyter_kernels`
- **Type:** `dict`
- **Default:** 
  ```python
  {
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
- **Purpose:** Defines kernel metadata written to notebook files
- **Notebook Target:** ✅ Essential - Jupyter needs this to run notebooks
- **Notes:** Can be extended for Julia, R, etc.

#### `tojupyter_default_lang`
- **Type:** `str`
- **Default:** `"python3"`
- **Purpose:** Default language when code block language is not specified
- **Notebook Target:** ✅ Essential
- **Notes:** Must match a key in `tojupyter_kernels`

#### `tojupyter_lang_synonyms`
- **Type:** `list`
- **Default:** `[]`
- **Purpose:** Treat alternative syntax names as the default language
- **Notebook Target:** ✅ Essential for mixed syntax projects
- **Example:** `["pycon", "ipython"]` treats these as Python

#### `tojupyter_conversion_mode`
- **Type:** `str`
- **Default:** `"all"`
- **Options:** `"all"` or `"code"`
- **Purpose:** 
  - `"all"`: Generate full notebooks with markdown cells and code
  - `"code"`: Generate notebooks with only code cells
- **Notebook Target:** ✅ Essential - determines notebook structure

---

### Content Control Options

#### `tojupyter_drop_solutions`
- **Type:** `bool`
- **Default:** `True`
- **Purpose:** Drop code blocks marked with `:class: solution`
- **Notebook Target:** ✅ Useful for exercise notebooks
- **Use Case:** Generate student versions without solutions

#### `tojupyter_drop_tests`
- **Type:** `bool`
- **Default:** `True`
- **Purpose:** Drop code blocks marked with `:class: test`
- **Notebook Target:** ✅ Useful for clean notebooks
- **Use Case:** Remove testing/validation code from user-facing notebooks

#### `tojupyter_drop_raw_html` 🆕
- **Type:** `bool`
- **Default:** `True`
- **Purpose:** Drop raw HTML/JavaScript blocks (e.g., Thebe configuration)
- **Notebook Target:** ✅ Essential for clean notebooks
- **Added:** This PR (commit 85e64da)
- **Why:** Prevents web-specific HTML/script tags appearing as markdown cells
- **Test Coverage:** `tests/raw_html/`

---

### Asset Handling Options

#### `tojupyter_static_file_path`
- **Type:** `list`
- **Default:** `[]`
- **Purpose:** Paths to static files/folders to copy to build directory
- **Notebook Target:** ✅ Useful for notebooks with local images/data
- **Example:** `["source/_static", "source/data"]`

#### `tojupyter_images_markdown`
- **Type:** `bool`
- **Default:** `True`
- **Purpose:** Use markdown `![](image.png)` syntax instead of HTML `<img>`
- **Notebook Target:** ✅ Recommended - cleaner markdown rendering
- **Note:** Disables RST `:scale:` option when enabled

---

### URL Path Options

#### `tojupyter_urlpath` 🔧
- **Type:** `str` or `None`
- **Default:** `None`
- **Purpose:** Base URL for cross-document notebook links
- **Notebook Target:** ✅ Essential for distributed notebooks
- **Fixed:** This PR - now properly prefixes internal cross-document links
- **Example:** `"https://lectures.quantecon.org/"`
- **Result:** Links become `https://lectures.quantecon.org/doc.ipynb#section`
- **Test Coverage:** `tests/urlpath/`

#### `tojupyter_image_urlpath`
- **Type:** `str` or `None`
- **Default:** `None`
- **Purpose:** Base URL for image references
- **Notebook Target:** ✅ Useful for hosted notebooks
- **Use Case:** Point images to CDN or website instead of relative paths
- **Example:** `"https://lectures.quantecon.org/_static/"`

#### `tojupyter_glue_urlpath`
- **Type:** `str` or `None`
- **Default:** `None`
- **Purpose:** Base URL for MyST-NB glue figure references
- **Notebook Target:** ✅ For MyST-NB glue feature
- **Use Case:** Similar to `tojupyter_image_urlpath` but for glued figures

---

### Advanced Options

#### `tojupyter_latex_macros`
- **Type:** `str` or `None`
- **Default:** `None`
- **Purpose:** Path to LaTeX macros file to inject into notebooks
- **Notebook Target:** ✅ Essential for consistent math rendering
- **Format:** YAML file with macro definitions
- **Injected:** As first cell in notebook for LaTeX math support

#### `tojupyter_dependency_lists`
- **Type:** `dict`
- **Default:** `{}`
- **Purpose:** Specify file/directory dependencies to copy
- **Notebook Target:** ✅ Useful for notebooks with data files
- **Format:**
  ```python
  {
      "directory": ["file1.csv", "file2.json"],
      "directory/file.rst": ["data.csv"]
  }
  ```

#### `tojupyter_nextprev_ignore` ⚠️
- **Type:** `list`
- **Default:** `[]`
- **Purpose:** Files to ignore for next/previous navigation
- **Notebook Target:** ⚠️ **NEEDS REVIEW**
- **Question:** Is this still relevant for v1.0 notebook-only focus?
- **Context:** May have been for HTML generation features

---

## Options Removed in v1.0

The following options were removed as part of the v1.0 refactor focusing on notebook generation:

### Execution-Related (removed)
- `jupyter_execute_notebooks` - Execution now handled by myst-nb/jupyter-book
- `jupyter_allow_errors` - Execution feature removed
- `jupyter_timeout` - Execution feature removed
- `jupyter_cache_execution` - Execution feature removed

### PDF-Related (removed)
- `jupyter_make_pdf` - PDF generation removed
- `jupyter_pdf_logo` - PDF feature removed
- `jupyter_pdf_author` - PDF feature removed
- `jupyter_pdf_urlpath` - PDF feature removed

### HTML/Website-Related (removed)
- `jupyter_make_site` - HTML generation removed
- `jupyter_template_coverage_file_path` - Coverage tracking removed
- `jupyter_template_header_file_path` - HTML template removed
- `jupyter_binder_url` - Binder integration removed
- `jupyter_jupyterhub_url` - JupyterHub integration removed
- `jupyter_download_nb` - Download button removed
- `jupyter_download_nb_urlpath` - Download feature removed
- `jupyter_lab_url` - JupyterLab integration removed
- `jupyter_coverage_dir` - Coverage feature removed

### Other Removed Features
- `jupyter_number_equations` - Equation numbering feature removed
- `jupyter_write_metadata` - Metadata writing simplified
- `jupyter_ignore_no_execute` - Execution-related
- `jupyter_ignore_skip_test` - Testing-related
- `jupyter_allow_html_only` - HTML-specific

---

## Recommendations for v1.0 Focus

### ✅ Options Aligned with Notebook Generation

All current options are properly focused on notebook generation:

1. **Core options** - Control kernel, language, and conversion mode
2. **Content control** - Drop specific content types (solutions, tests, raw HTML)
3. **Asset handling** - Manage images and static files
4. **URL paths** - Link notebooks together and to external resources
5. **Advanced** - LaTeX macros and dependencies

### ⚠️ Options Needing Review

#### `tojupyter_nextprev_ignore`
- **Current Status:** Listed but unclear usage
- **Question:** What does "next/prev navigation" mean in notebook context?
- **Action:** 
  - If it controls notebook ordering/linking → Keep and document
  - If it's legacy HTML feature → Remove
  - **Recommendation:** Search codebase for usage and decide

---

## Testing Coverage

### ✅ Well-Tested Options

1. **Core Generation** - Tested via `tests/base/` (26 files)
2. **URL Paths** - Dedicated test suite `tests/urlpath/`
3. **Raw HTML Drop** - Dedicated test suite `tests/raw_html/`
4. **MyST Features** - Test suite `tests/myst_features/`

### ⚠️ Options Needing Test Coverage

Consider adding dedicated tests for:
1. `tojupyter_lang_synonyms` - Verify synonym handling
2. `tojupyter_conversion_mode = "code"` - Verify code-only mode
3. `tojupyter_drop_solutions` / `tojupyter_drop_tests` - Verify dropping behavior
4. `tojupyter_static_file_path` - Verify file copying
5. `tojupyter_dependency_lists` - Verify dependency handling
6. `tojupyter_latex_macros` - Verify LaTeX injection

---

## Migration Notes

For users upgrading from older versions:

### Renamed Options (v0.x → v1.0)

Most options were renamed from `jupyter_*` to `tojupyter_*`:

- `jupyter_kernels` → `tojupyter_kernels`
- `jupyter_default_lang` → `tojupyter_default_lang`
- `jupyter_conversion_mode` → `tojupyter_conversion_mode`
- etc.

### New Options in v1.0

- `tojupyter_drop_raw_html` - New in this PR

### Configuration Migration

See `MIGRATION.md` for complete migration guide from v0.x to v1.0.

---

## Summary

**Total Active Options:** 15  
**Well-Tested:** 11  
**Need Review:** 1 (`tojupyter_nextprev_ignore`)  
**Need Testing:** 4-5 (minor features)

**Overall Assessment:** ✅ Configuration is well-aligned with v1.0 focus on notebook generation. All options serve clear purposes for creating clean, functional Jupyter notebooks from RST/MyST source files.
