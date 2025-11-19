# Raw HTML Drop Test Suite

This test suite verifies that the `tojupyter_drop_raw_html` configuration option correctly handles raw HTML blocks in generated notebooks.

## Purpose

Prevent web-specific content (like Thebe configuration, JavaScript, custom HTML) from appearing in Jupyter notebooks where it serves no purpose and may confuse users.

## Configuration

The test uses this setting in `conf.py`:

```python
tojupyter_drop_raw_html = True  # Default behavior
```

## Test Files

- `index.rst` - Main index
- `with_raw_html.rst` - Document with raw HTML blocks (Thebe config, scripts, divs)

## Running Tests

```bash
cd tests/raw_html
make jupyter
```

## Verification

After building, check the generated notebook in `_build/jupyter/`:

### Expected Results

**Content that SHOULD appear:**
- Regular markdown text
- Code blocks
- Headings and sections

**Content that should NOT appear:**
- `<script type="text/x-thebe-config">` blocks
- `<script>kernelName = ...</script>` tags
- `<div class="thebe-status"></div>` elements
- Any other raw HTML content

### Manual Verification

```bash
# Check that Thebe config is NOT in the notebook
grep -i "thebe" _build/jupyter/with_raw_html.ipynb

# Should return no matches or only in comments
```

Or open the notebook:

```bash
jupyter notebook _build/jupyter/with_raw_html.ipynb
```

## Automated Testing

This test can be run via nox:

```bash
nox -s test-raw-html
```

The test will:
1. Build the notebooks
2. Parse the generated JSON
3. Verify no raw HTML content is present
4. Report any issues

## Use Case

This addresses the issue where Jupyter Book / MyST projects include Thebe configuration in source files, and that configuration was appearing as extra markdown cells at the end of generated notebooks.

### Example Issue

**Before fix:**
- Notebook has 28 cells
- Last cell contains:
  ```html
  <script type="text/x-thebe-config">
  { requestKernel: true, ... }
  </script>
  ```

**After fix:**
- Notebook has 27 cells
- No raw HTML/script content
- Clean, user-friendly output

## Configuration Override

If you need to preserve raw HTML (e.g., for round-trip conversion), set:

```python
# conf.py
tojupyter_drop_raw_html = False
```

**Note:** Most users should keep the default (`True`) for clean notebook output.
