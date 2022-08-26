.. _checklist:

checklist module
================

.. py:module:: pyobis.checklist

.. autoclass:: OBISQueryResult

An OBISQueryResult object for fetching checklist records.

Usage
#####

.. code-block:: python

    from pyobis.checklist import OBISQueryResult as OQR

    query = OQR()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: OBISQueryResult.list
.. automethod:: OBISQueryResult.redlist
.. automethod:: OBISQueryResult.newest
.. automethod:: OBISQueryResult.get_search_url
.. automethod:: OBISQueryResult.get_mapper_url
