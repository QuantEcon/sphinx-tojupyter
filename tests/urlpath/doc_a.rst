Document A: Cross-Document Links
==================================

This document tests cross-document references with `tojupyter_urlpath` configured.

.. _doc-a-section-1:

Section 1: Link to Document B
------------------------------

Here is a cross-document link to :doc:`doc_b`. With the configured `tojupyter_urlpath`, 
this should become: `https://continuous-time-mcs.quantecon.org/doc_b.ipynb`

Here is a link to a specific section in document B: :ref:`doc-b-section-2`.
This should become: `https://continuous-time-mcs.quantecon.org/doc_b.ipynb#doc-b-section-2`

.. _doc-a-section-2:

Section 2: In-Page Anchor
--------------------------

Here is an in-page link to :ref:`doc-a-section-1` (above).
This should remain a local anchor: `#doc-a-section-1`

And a link back to itself: :ref:`doc-a-section-2`.
This should also remain a local anchor: `#doc-a-section-2`

.. _doc-a-exercise-1:

Exercise 1
----------

This is an exercise that will be referenced from Document B.

The solution is below.

.. _doc-a-solution-1:

Solution to Exercise 1
~~~~~~~~~~~~~~~~~~~~~~

This is the solution to Exercise 1.

External Links
--------------

Here is an external link that should not be modified: 
`QuantEcon <https://quantecon.org>`_

Code Example
------------

.. code-block:: python

   # Some Python code
   def hello():
       return "Hello World"
   
   print(hello())
