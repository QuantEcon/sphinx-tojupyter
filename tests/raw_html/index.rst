Raw HTML Drop Test
==================

.. toctree::
   :maxdepth: 2

   with_raw_html

Test Suite
----------

This test verifies that raw HTML blocks (like Thebe configuration) are dropped from generated notebooks by default.

Expected Behavior
-----------------

**With `tojupyter_drop_raw_html = True` (default):**

- Raw HTML blocks are not included in notebooks
- Script tags (Thebe config, etc.) are dropped
- Only content visible in notebooks remains

**With `tojupyter_drop_raw_html = False`:**

- Raw HTML is preserved in markdown cells
- Useful for round-trip conversion workflows
