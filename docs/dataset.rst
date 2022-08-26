.. _dataset:

dataset module
================

.. py:module:: pyobis.dataset

.. autoclass:: OBISQueryResult

An OBISQueryResult object for fetching dataset records.

Usage
#####

.. code-block:: python

    from pyobis.dataset import OBISQueryResult as OQR

    query = OQR()
    data = dataset.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: OBISQueryResult.get
.. automethod:: OBISQueryResult.search
