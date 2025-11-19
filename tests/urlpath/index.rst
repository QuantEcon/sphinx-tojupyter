# URL Path Test Suite

Test Suite Documentation
========================

This test suite verifies that the `tojupyter_urlpath` and `tojupyter_image_urlpath` configuration options work correctly.

.. toctree::
   :maxdepth: 2

   doc_a
   doc_b

Expected Behavior
-----------------

Cross-document links
~~~~~~~~~~~~~~~~~~~~

When `tojupyter_urlpath` is set to `https://continuous-time-mcs.quantecon.org/`:

- Links to other documents should be prefixed with the base URL
- Example: `doc_b.ipynb` becomes `https://continuous-time-mcs.quantecon.org/doc_b.ipynb`
- Links with anchors: `doc_b.ipynb#section-id` becomes `https://continuous-time-mcs.quantecon.org/doc_b.ipynb#section-id`

In-page anchors
~~~~~~~~~~~~~~~

Anchors to sections within the same document should remain as local anchors:

- `#section-id` remains `#section-id`
- These are NOT prefixed with the base URL

External links
~~~~~~~~~~~~~~

External links (starting with `http://` or `https://`) should not be modified.

Testing
-------

Run the tests:

.. code-block:: bash

   cd tests/urlpath
   make jupyter
   
Then inspect the generated notebooks in `_build/jupyter/` to verify link formatting.
