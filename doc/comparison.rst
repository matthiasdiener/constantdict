Comparison of ``dict`` implementations
======================================

Performance
-----------

Code
****

These results were generated with the following code, found in
`examples/speed.py <https://github.com/matthiasdiener/constantdict/blob/main/examples/speed.py>`__ in the
source distribution:

.. raw:: html

    <details>

.. literalinclude:: ../examples/speed.py
   :language: python

.. raw:: html

    </details>

Results
*******

Results (total time of 10,000 executions) for Python 3.11 on a Mac M1:

.. image:: dict_performance_small.png
    :width: 90%
    :alt: dict performance small


.. image:: dict_performance_large.png
    :width: 90%
    :alt: dict performance large
