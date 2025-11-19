Document with Raw HTML Blocks
==============================

This document contains raw HTML blocks that should be dropped by default.

Regular Content
---------------

This is regular content that should appear in the notebook.

.. code-block:: python

   # Some Python code
   def hello():
       return "Hello, World!"
   
   print(hello())

Raw HTML Block (Thebe Config)
-------------------------------

Below is a raw HTML block containing Thebe configuration. This should NOT appear
in the generated notebook when `tojupyter_drop_raw_html = True`.

.. raw:: html

   <script type="text/x-thebe-config">
   {
       requestKernel: true,
       binderOptions: {
           repo: "binder-examples/jupyter-stacks-datascience",
           ref: "master",
       },
       codeMirrorConfig: {
           theme: "abcdef",
           mode: "python"
       },
       kernelOptions: {
           name: "python3",
           path: "./."
       },
       predefinedOutput: true
   }
   </script>

   <script>kernelName = 'python3'</script>

More Regular Content
--------------------

This content should also appear in the notebook.

Another Raw HTML Block
----------------------

.. raw:: html

   <div class="thebe-status"></div>
   <button class="thebe-button thebe-launch-button">Launch Thebe</button>

Final Section
-------------

This is the final section of regular content.

**Expected Result:** The generated notebook should have:

1. Regular content sections
2. Code blocks
3. NO raw HTML blocks
4. NO script tags
5. Clean, user-friendly output
