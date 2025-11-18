# Testing sphinx-proof Support Against QuantEcon Lectures

This guide helps you test the sphinx-proof implementation against real QuantEcon lecture repositories.

## Quick Start

### 1. Setup This Branch

```bash
cd /path/to/sphinx-tojupyter
git checkout add-sphinx-proof-support
pip install -e ".[dev]"
```

### 2. Clone a QuantEcon Lecture Repository

Choose one that uses sphinx-proof:

```bash
# Example: Python lectures
cd ~/work/quantecon
git clone https://github.com/QuantEcon/lecture-python.quantecon.org
cd lecture-python.quantecon.org
```

### 3. Update to Use Local sphinx-tojupyter

Edit the project's `environment.yml` or `requirements.txt` to use your local development version:

```yaml
# In environment.yml, comment out the pip install line:
# - pip:
#   - sphinx-tojupyter

# Or manually install after creating environment:
conda env create -f environment.yml
conda activate lecture-python
pip uninstall sphinx-tojupyter -y
pip install -e /path/to/sphinx-tojupyter
```

### 4. Build Notebooks

```bash
make jupyter
```

Or:

```bash
sphinx-build -b jupyter source _build/jupyter
```

### 5. Check for sphinx-proof Content

Look for files that use sphinx-proof directives:

```bash
# Find source files with proof directives
grep -r "prf:theorem\|prf:proof\|prf:lemma" source/
```

Then check the corresponding generated notebooks:

```bash
# Open in JupyterLab
jupyter lab _build/jupyter/
```

## What to Verify

### ✅ Content Completeness

- [ ] All theorem statements appear in notebooks
- [ ] All proof content is present
- [ ] No missing definitions, lemmas, or axioms
- [ ] Algorithm steps are readable

### ✅ Formatting Quality

- [ ] Headers are bold and properly formatted
- [ ] Numbering is correct and sequential
- [ ] Titles display in parentheses
- [ ] Math notation renders properly
- [ ] No duplicate content

### ✅ Expected Format

Theorems should look like:

```markdown
**Theorem 1** (Optional Title)

Statement of the theorem with $math$ notation...
```

Proofs should look like:

```markdown
**Proof.**

Proof content here...
```

### ✅ Edge Cases

- [ ] Unnumbered directives (with `:nonumber:`)
- [ ] Directives without titles
- [ ] Nested math environments
- [ ] Cross-references between directives
- [ ] Multiple directives in one document

## Common Issues and Solutions

### Issue: "No module named 'sphinx_tojupyter'"

**Solution:**
```bash
pip uninstall sphinx-tojupyter -y
cd /path/to/sphinx-tojupyter
pip install -e .
```

### Issue: Old cached build

**Solution:**
```bash
make clean
rm -rf _build
make jupyter
```

### Issue: Missing directive content

**Check:**
1. Is sphinx-proof installed? `pip list | grep sphinx-proof`
2. Is it in extensions? Check `conf.py` for `sphinx_proof`
3. Is numfig enabled? Check `conf.py` for `numfig = True`

### Issue: Double parentheses in titles

This was fixed in the implementation. If you see it:
```bash
# Make sure you have the latest version
cd /path/to/sphinx-tojupyter
git pull origin add-sphinx-proof-support
pip install -e . --force-reinstall
```

## Reporting Results

After testing, please report:

### Good Output

If notebooks look correct:
```markdown
✅ Tested against: lecture-python.quantecon.org
✅ Branch: main
✅ Files checked: [list key files]
✅ All directives render correctly
✅ No missing content
✅ Formatting looks professional
```

### Issues Found

If you find problems:
```markdown
❌ Issue: [Brief description]
📁 File: source/path/to/file.md
🔍 Expected: [What you expected]
👀 Got: [What you actually saw]
📎 Attach: Screenshots or notebook snippets
```

## Testing Checklist

### Core Functionality
- [ ] Build completes without errors
- [ ] All notebooks generate successfully
- [ ] No warnings about missing content

### Directive Types (if present in lectures)
- [ ] Theorems appear and are numbered
- [ ] Proofs appear after theorems
- [ ] Lemmas are formatted correctly
- [ ] Definitions are complete
- [ ] Examples are readable
- [ ] Algorithms preserve structure

### Math Content
- [ ] Inline math ($...$) works
- [ ] Display math ($$...$$) works
- [ ] Equation numbering preserved
- [ ] LaTeX macros work (if defined)

### References
- [ ] Internal links work
- [ ] Cross-references to theorems work
- [ ] Labels are preserved

## Advanced Testing

### Test with nox

From the sphinx-tojupyter directory:

```bash
# Run the full test suite
nox -s tests-full

# Just test sphinx-proof
nox -s test-proof

# Test on specific Python version
nox -s tests-3.11
```

### Compare Before/After

1. Build with main branch
2. Save a notebook: `cp _build/jupyter/important.ipynb /tmp/before.ipynb`
3. Checkout this PR branch
4. Rebuild: `make clean && make jupyter`
5. Compare: `nbdime diff /tmp/before.ipynb _build/jupyter/important.ipynb`

### Performance Check

```bash
# Time the build
time make jupyter

# Check memory usage
/usr/bin/time -l make jupyter  # macOS
/usr/bin/time -v make jupyter  # Linux
```

## Repositories to Test

Priority list of QuantEcon repositories that likely use sphinx-proof:

1. **lecture-python.quantecon.org** - Main Python lectures
2. **lecture-python-advanced.quantecon.org** - Advanced topics
3. **lecture-julia.quantecon.org** - Julia lectures
4. **quantecon-example** - If it exists

Check each repo's documentation for build instructions.

## Questions?

Add comments to the PR: https://github.com/QuantEcon/sphinx-tojupyter/pull/61
