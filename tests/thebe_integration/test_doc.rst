Test Document with Thebe
========================

This document simulates what happens when sphinx-thebe is enabled.

Introduction
------------

This is a test document to verify that raw HTML blocks (like Thebe configuration)
are properly dropped from generated notebooks.

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

Content After Script
--------------------

This content should appear in the notebook, but the script tags above should NOT.

.. code-block:: python

   print("Hello from Python!")
   x = 42

Another Raw HTML Block
----------------------

.. raw:: html

   <div class="thebe-activate">
       <button class="thebe-button">Activate Thebe</button>
   </div>

Final Section
-------------

This is the end of the document.

**Expected Result:** The notebook should contain:
- This markdown content
- The Python code block
- NO script tags
- NO Thebe button HTML
