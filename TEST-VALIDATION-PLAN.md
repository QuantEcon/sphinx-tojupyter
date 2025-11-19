# Test Validation Plan for v2.0 Refactoring

## Summary
We've removed 220 lines of PDF/HTML/book_index logic from the translators. Now we need to validate that:
1. All existing tests still pass
2. Reference notebooks may need updating due to simplified output
3. No regressions in core functionality

## What We Changed
- Removed `tojupyter_target_pdf` and `tojupyter_target_html` conditionals
- Removed book index construction logic
- Removed PDF-specific formatting (LaTeX commands, special math spacing)
- Simplified `depart_reference` from 143 to 45 lines
- Always use Markdown-style links and formatting

## Expected Impact on Tests

### Base Tests (`tests/base/`)
**Likely Changes Needed:**
- `links.rst` / `links_target.rst` - Link format may have changed (no more `.html` extensions)
- `footnotes.rst` - Footnote links simplified (removed HTML branch)
- `math.rst` - Math spacing may differ (removed PDF "${}$" vs "$ {} $" logic)
- `equation_labels.rst` - Equation references simplified (no more PDF \eqref)

**Should Be Unchanged:**
- Code blocks
- Lists
- Tables
- Images
- Most text formatting

### Glue Tests (`tests/glue/`)
**Status:** Should be unaffected (no PDF/HTML logic in glue handling)

### Sphinx-Proof Tests (`tests/sphinx_proof/`)
**Status:** Should be unaffected (no PDF/HTML logic in proof handling)

## Validation Steps

### Step 1: Run Base Tests with Diff Check
```bash
# In nox session to get clean virtualenv
nox -s "tests-3.13(sphinx='8.2')"
```

**Expected Outcome:** May fail on some notebooks due to output format changes

### Step 2: Visual Inspection
If tests fail, manually inspect the differences:
```bash
cd tests/base
# Compare a few key files:
jupyter nbdiff ipynb/links.ipynb _build/jupyter/links.ipynb
jupyter nbdiff ipynb/footnotes.ipynb _build/jupyter/footnotes.ipynb
jupyter nbdiff ipynb/math.ipynb _build/jupyter/math.ipynb
```

**Key Questions:**
- Are links still functional? (just different format is OK)
- Is math still rendering correctly?
- Are footnotes working?
- Any missing content?

### Step 3: Update Reference Notebooks (if needed)
If the changes are correct (just simplified output), update references:
```bash
cd tests/base
# Back up old references
cp -r ipynb ipynb.backup

# Copy new output as references
rm -rf ipynb
mkdir ipynb
cp _build/jupyter/*.ipynb ipynb/

# Review changes
git diff ipynb/

# If good, commit
git add ipynb/
git commit -m "test: update reference notebooks for v2.0 simplified output"
```

### Step 4: Full Test Matrix
Once base tests pass:
```bash
# Test all Python/Sphinx combinations
nox -s tests

# Test with full dependencies
nox -s tests-full

# Individual feature tests
nox -s test-glue
nox -s test-proof
```

## Critical Tests to Verify

### 1. Link Handling ⭐⭐⭐
**Why Critical:** We removed all HTML/PDF branching in `depart_reference`
**Test Files:** `links.rst`, `links_target.rst`, `math.rst` (eq refs)
**What to Check:**
- Internal links work (`.ipynb` extension added correctly)
- In-page anchors work (with `%28`/`%29` for parentheses)
- External links work
- Equation references work (`:eq:` directive)

### 2. Footnotes ⭐⭐
**Why Critical:** We simplified `visit_footnote_reference` 
**Test Files:** `footnotes.rst`
**What to Check:**
- Footnote references render
- Links to footnotes work
- Back-references work

### 3. Math Rendering ⭐⭐
**Why Critical:** We removed PDF spacing logic
**Test Files:** `math.rst`, `equation_labels.rst`
**What to Check:**
- Inline math renders (spacing OK)
- Display math renders
- Labeled equations work
- References to equations work

### 4. Lists ⭐
**Why Critical:** We removed `content_depth` skip logic
**Test Files:** `lists.rst`
**What to Check:**
- All list items present
- Nesting works correctly

### 5. Raw HTML ⭐
**Why Critical:** We removed `tojuyter_drop_html_raw` logic
**Test Files:** Check if any tests use `.. raw:: html`
**What to Check:**
- Raw HTML passed through (not dropped)

## Decision Points

### If Base Tests Fail:
**Option A: Update References** (recommended if output is correct but different)
- Pro: Reflects new v2.0 behavior
- Con: Loses old behavior for comparison
- Action: Update ipynb/ with new output

**Option B: Fix Code** (if output is actually broken)
- Pro: Maintains compatibility
- Con: May not be necessary for v2.0 goals
- Action: Review and fix translator logic

### If Glue/Proof Tests Fail:
**Action:** Fix immediately - these shouldn't be affected by our changes

### If Tests Are Slower:
- Document performance
- Consider optimization in future release

## Success Criteria
✅ All nox test sessions pass
✅ No broken links in notebooks
✅ No missing content
✅ Math renders correctly
✅ Reference notebooks updated and committed (if needed)
✅ CI pipeline green

## Timeline
1. Run Step 1 - 5 min
2. Inspect differences - 15 min
3. Update references (if needed) - 10 min
4. Full test matrix - 20 min
5. Documentation - 10 min

**Total: ~1 hour**

