# Thebe Integration Test

This test verifies that `tojupyter_drop_raw_html` configuration works correctly with raw HTML blocks (like those injected by sphinx-thebe).

## Test Files

- `test_doc.rst` - Document with raw HTML blocks (script tags, buttons, etc.)
- `conf.py` - Configuration with `tojupyter_drop_raw_html = True` (default)
- `conf_passthrough.py` - Configuration with `tojupyter_drop_raw_html = False`

## Running Tests

### Test 1: Verify raw HTML is dropped (default behavior)

```bash
cd tests/thebe_integration
sphinx-build -b jupyter . _build/jupyter
```

**Expected:** No `<script>` tags or HTML in the generated notebook.

### Test 2: Verify raw HTML passes through when disabled

```bash
cd tests/thebe_integration
sphinx-build -b jupyter -D tojupyter_drop_raw_html=0 . _build/jupyter_passthrough
```

**Expected:** `<script>` tags and HTML preserved in the generated notebook.

## Automated Comparison Test

Run from repository root:

```bash
# Build both versions
rm -rf tests/thebe_integration/_build
sphinx-build -b jupyter tests/thebe_integration tests/thebe_integration/_build/jupyter
sphinx-build -b jupyter -D tojupyter_drop_raw_html=0 tests/thebe_integration tests/thebe_integration/_build/jupyter_passthrough

# Compare results
python3 << 'EOF'
import json
import re

# Load both notebooks
with open('tests/thebe_integration/_build/jupyter/test_doc.ipynb') as f:
    nb_drop = json.load(f)
with open('tests/thebe_integration/_build/jupyter_passthrough/test_doc.ipynb') as f:
    nb_pass = json.load(f)

# Check for scripts
scripts_drop = sum(1 for c in nb_drop['cells'] 
                   if '<script' in ''.join(c.get('source', [])))
scripts_pass = sum(1 for c in nb_pass['cells'] 
                   if '<script' in ''.join(c.get('source', [])))

print(f'drop_raw_html=True:  {scripts_drop} scripts (expected: 0)')
print(f'drop_raw_html=False: {scripts_pass} scripts (expected: >0)')

if scripts_drop == 0 and scripts_pass > 0:
    print('✅ Test PASSED')
else:
    print('❌ Test FAILED')
EOF
```

## What This Tests

1. **Default Behavior (drop_raw_html=True):**
   - Raw HTML blocks are skipped during conversion
   - Thebe configuration scripts don't appear in notebooks
   - Buttons and divs are removed
   - Clean, user-friendly notebooks

2. **Passthrough Mode (drop_raw_html=False):**
   - Raw HTML blocks are preserved
   - Useful for round-trip conversion
   - May be needed for specific workflows

## Real-World Use Case

This test simulates what happens with projects using `sphinx-thebe` (included in Jupyter Book):

- sphinx-thebe injects `<script>` tags for Thebe configuration
- Without `tojupyter_drop_raw_html=True`, these scripts appear as markdown cells
- With `tojupyter_drop_raw_html=True` (default), scripts are cleanly removed

## Comparison with v0.6.0

- **v0.6.0 (main branch):** Had the feature but with typo `tojuyter_drop_html_raw`
- **v1.0-refactor (before fix):** Accidentally removed during refactoring - raw HTML passed through
- **v1.0-refactor (after fix):** Restored with correct name `tojupyter_drop_raw_html`
