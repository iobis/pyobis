.. _dataset:

dataset module
================

.. py:module:: pyobis.dataset

.. autoclass:: DatasetQuery

A DatasetQuery object for fetching dataset records.

Usage
#####

.. code-block:: python

    from pyobis.dataset import DatasetQuery

    query = DatasetQuery()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: DatasetQuery.get
.. automethod:: DatasetQuery.search
.. automethod:: DatasetQuery.get_search_url
.. automethod:: DatasetQuery.get_mapper_url
