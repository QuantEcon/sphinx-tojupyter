# Future Development Plan

**Project:** sphinx-tojupyter  
**Current Version:** v1.0.0  
**Document Purpose:** Track planned enhancements and feature roadmap

---

## v1.x Roadmap - Incremental Improvements

### v1.1.0 - Enhanced MyST Admonitions

**Goal:** Add full support for all MyST admonition types

**Current State:**
- ✅ `{note}` - Works with blockquote formatting
- ⚠️ Other admonitions render as plain text (content preserved, formatting lost)

**Planned Features:**
- [ ] Add handlers for warning, tip, important, caution, danger
- [ ] Add handlers for error, hint, seealso
- [ ] Consistent blockquote formatting with type indicators
- [ ] Custom admonition support with proper titles

**Implementation:**
```python
# In translators/full.py
def visit_warning(self, node):
    self.add_text('>**Warning**\n>\n')
    
def depart_warning(self, node):
    pass
```

**Test Coverage:**
- [ ] Update `tests/myst_features/` with expected admonition output
- [ ] Add validation tests for all admonition types
- [ ] Test nested admonitions

**Estimated Effort:** Small (~2-4 hours)

---

### v1.2.0 - Code Block Options

**Goal:** Support code block options for improved teaching materials

**Current State:**
- ⚠️ `:linenos:` - Ignored
- ⚠️ `:caption:` - Becomes separate paragraph (acceptable but not ideal)
- ⚠️ `:emphasize-lines:` - Ignored

**Planned Features:**
- [ ] Line number support (render as commented numbers or prefix)
- [ ] Caption integration (keep as separate paragraph or improve)
- [ ] Line emphasis (use markdown annotations or comments)

**Implementation Options:**

1. **Line Numbers:**
   ```python
   # Option A: Inline comments
   # 1: def hello():
   # 2:     print("world")
   
   # Option B: Markdown table
   | Line | Code |
   |------|------|
   | 1 | def hello(): |
   | 2 |     print("world") |
   ```

2. **Emphasis:**
   ```python
   # Option: Use comments
   def hello():
       print("world")  # ← emphasized
       return 42       # ← emphasized
   ```

**Considerations:**
- Jupyter notebooks have limited code block formatting
- Solutions must work in both notebook editors and rendered HTML
- May need to document as "best effort" feature

**Test Coverage:**
- [ ] Test line numbers with various code lengths
- [ ] Test captions with special characters
- [ ] Test emphasis with multiple line ranges

**Estimated Effort:** Medium (~4-8 hours)

---

### v1.3.0 - Advanced MyST Features

**Goal:** Support additional MyST-specific syntax elements

**Current State:**
- ❌ Fence-style directives (`:::note`)
- ❌ Special inline roles (`{kbd}`, `{file}`, `{abbr}`)
- ⚠️ Nested directives (split into multiple cells)

**Planned Features:**

1. **Fence-style Directives:**
   - [ ] Parse `:::directive` syntax
   - [ ] Convert to standard directive handling
   - [ ] Test equivalence with `\`\`\`{directive}` syntax

2. **Inline Roles:**
   - [ ] `{kbd}` → Monospace or quoted text
   - [ ] `{file}` → Italicized file paths
   - [ ] `{abbr}` → Expanded abbreviations in parentheses
   - [ ] `{menuselection}` → Menu path formatting
   - [ ] `{guilabel}` → GUI label formatting

3. **Nested Directive Improvements:**
   - [ ] Keep code blocks inside admonitions in same cell
   - [ ] Preserve list continuity across nested elements
   - [ ] Maintain visual grouping

**Implementation Considerations:**
- Inline roles need to map to Markdown-compatible formatting
- Nested directives may require tracking directive depth
- Some features may need "best effort" approximations

**Test Coverage:**
- [ ] Comprehensive test file for all inline roles
- [ ] Nested directive test cases
- [ ] Fence-style syntax equivalence tests

**Estimated Effort:** Large (~8-16 hours)

---

## v2.x Roadmap - Future Major Changes

Reserved for potential major architecture changes. Currently no plans.

Possible future needs:
- Complete rewrite for different Sphinx architecture
- Major API changes
- Fundamental conversion algorithm changes

---

## Known Limitations (Documented)

### MyST Features - Acceptable Limitations

These features work but with graceful degradation:

1. **Other Admonitions** (warning, tip, etc.)
   - Content preserved as plain text
   - No special formatting or blockquote
   - **Workaround:** Use `{note}` with emoji/text indicators
   - **Future:** v1.1.0 will add full support

2. **Code Block Options**
   - `:linenos:` ignored
   - `:caption:` becomes separate paragraph
   - `:emphasize-lines:` ignored
   - **Workaround:** Add line numbers as comments
   - **Future:** v1.2.0 will improve support

3. **Nested Directives**
   - Code blocks split into separate cells
   - List continuity may break
   - Content always preserved
   - **Future:** v1.3.0 will improve handling

### By Design - Not Planned

These features are out of scope by design:

1. **PDF Generation** - Use Jupyter Book
2. **HTML Website Generation** - Use Jupyter Book
3. **Notebook Execution** - Use Jupyter Book or nbconvert
4. **Coverage Tracking** - Use pytest-cov or coverage.py

---

## Contributing Guidelines

### Adding New Features

1. **Identify the need:**
   - User request or common use case
   - Check if feature fits v1.x scope (notebook generation only)

2. **Plan the implementation:**
   - Add to this document with version target
   - Estimate effort and complexity
   - Consider Jupyter notebook limitations

3. **Implementation checklist:**
   - [ ] Add visitor/depart methods if needed
   - [ ] Update relevant translators
   - [ ] Add comprehensive tests
   - [ ] Update documentation
   - [ ] Add to CHANGELOG.md

4. **Testing requirements:**
   - All existing tests must pass
   - New feature has specific test coverage
   - Test with multiple Python/Sphinx versions
   - Validate notebook output manually

5. **Documentation requirements:**
   - Update relevant docs/ files
   - Add examples to test suite
   - Update README if major feature
   - Add migration notes if needed

### Code Quality Standards

Before submitting features:

- [ ] All functions have docstrings (Google/NumPy style)
- [ ] No Python 2 compatibility code
- [ ] Consistent error handling (use logger.warning or raise)
- [ ] Type hints for public APIs
- [ ] Follow existing code style
- [ ] No dead code or commented-out blocks

---

## Research & Investigation

### Areas for Future Exploration

1. **Performance Optimization**
   - Profile large document conversion times
   - Identify bottlenecks in node traversal
   - Consider parallel processing for multi-file projects

2. **Better MyST-Parser Integration**
   - Investigate direct MyST AST access
   - Reduce reliance on Sphinx docutils nodes
   - Potential for cleaner MyST-specific handling

3. **Jupyter Notebook Standards**
   - Track nbformat specification updates
   - Monitor Jupyter notebook rendering improvements
   - Identify new possibilities for rich formatting

4. **User Feedback**
   - Collect common pain points
   - Identify most-requested features
   - Prioritize based on user impact

---

## Version History

| Version | Released | Focus |
|---------|----------|-------|
| v0.6.0 | 2023 | Multi-purpose tool (PDF/HTML/execution) |
| v1.0.0 | 2024-11-19 | Focused notebook generation |
| v1.1.0 | TBD | Enhanced MyST admonitions |
| v1.2.0 | TBD | Code block options |
| v1.3.0 | TBD | Advanced MyST features |
| v2.0.0 | Future | Reserved for major changes |

---

## Quick Reference

### Current Feature Status

| Feature | Status | Version |
|---------|--------|---------|
| RST → Notebook | ✅ Full | v1.0.0 |
| MyST → Notebook | ✅ Full | v1.0.0 |
| MyST-NB Glue | ✅ Full | v1.0.0 |
| sphinx-proof | ✅ Full | v1.0.0 |
| Note admonitions | ✅ Full | v1.0.0 |
| Other admonitions | ⚠️ Partial | → v1.1.0 |
| Code block options | ⚠️ Partial | → v1.2.0 |
| Inline roles | ❌ Missing | → v1.3.0 |
| Nested directives | ⚠️ Partial | → v1.3.0 |

### Getting Started with Contributions

1. Read this document
2. Check open issues on GitHub
3. Review [REFACTOR-PLANNING.md](REFACTOR-PLANNING.md) for architecture context
4. Set up development environment (see tests/README.md)
5. Run full test suite before and after changes
6. Submit PRs with tests and documentation

---

**Last Updated:** 2024-11-19  
**Maintainer:** QuantEcon team
