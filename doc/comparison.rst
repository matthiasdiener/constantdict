Comparison of ``dict`` implementations
======================================

Features
--------

.. list-table::
   :header-rows: 1

   * - Package
     - License
     - Deterministic iteration order
     - Frozen/Immutable
   * - :class:`dict`
     - ✅ PSF
     - ✅
     - ❌
   * - `constantdict <https://github.com/matthiasdiener/constantdict>`__
     - ✅ MIT
     - ✅
     - ✅
   * - `immutabledict <https://github.com/corenting/immutabledict>`__
     - ✅ MIT
     - ✅
     - ✅
   * - `immutables.Map <https://github.com/MagicStack/immutables>`__
     - ✅ Apache 2.0
     - ❌
     - ✅
   * - `frozendict <https://github.com/Marco-Sulla/python-frozendict>`__
     - ❌ LGPL-3.0
     - ✅
     - ✅

   * - `pyrsistent.PMap <https://github.com/tobgu/pyrsistent>`__
     - ✅ MIT
     - ❌
     - ✅


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
