Document B: More Cross-References
===================================

This document tests more cross-document and in-page references.

.. _doc-b-section-1:

Section 1: Link Back to Document A
-----------------------------------

Here is a cross-document link back to :doc:`doc_a`. 
This should become: `https://continuous-time-mcs.quantecon.org/doc_a.ipynb`

Here is a link to a specific section in Document A: :ref:`doc-a-section-2`.
This should become: `https://continuous-time-mcs.quantecon.org/doc_a.ipynb#doc-a-section-2`

.. _doc-b-section-2:

Section 2: Exercise Reference
------------------------------

See :ref:`doc-a-exercise-1` for an exercise, and :ref:`doc-a-solution-1` for the solution.

Both of these should be prefixed with the base URL since they reference another document.

.. _doc-b-exercise-1:

Exercise in Document B
----------------------

This is an exercise in document B.

Link to the solution below: :ref:`doc-b-solution-1`.
This should be a local anchor since it's in the same document.

.. _doc-b-solution-1:

Solution
~~~~~~~~

This is the solution. Link back to the exercise: :ref:`doc-b-exercise-1`.
Also a local anchor.

Mixed Links
-----------

- Cross-document link: :ref:`doc-a-section-1` (should have base URL)
- In-page link: :ref:`doc-b-section-1` (should be local anchor)
- Another in-page link: :ref:`doc-b-section-2` (should be local anchor)
- External link: `Sphinx Documentation <https://www.sphinx-doc.org/>`_ (should not be modified)

Numbered List with Links
-------------------------

1. First item with link to :ref:`doc-a-exercise-1` (cross-document)
2. Second item with link to :ref:`doc-b-exercise-1` (in-page)
3. Third item with external link `Python <https://www.python.org/>`_

Code Block
----------

.. code-block:: python

   # Testing code blocks
   import numpy as np
   
   def calculate():
       return np.array([1, 2, 3])
   
   result = calculate()
   print(result)
