.. _dataset:

dataset module
================

.. py:module:: pyobis.dataset

.. autoclass:: DatasetResponse

Usage
#####

.. code-block:: python

    from pyobis import dataset

    query = dataset.search(args, **kwargs)  # Build the Query
    query.execute()  # Execute the Query
    query.data  # Returns the data

    # or build and execute at the same time
    data = dataset.search(args, **kwargs).execute()

Methods:
########

.. autofunction:: get
.. autofunction:: search
