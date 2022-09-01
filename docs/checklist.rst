.. _checklist:

checklist module
================

.. py:module:: pyobis.checklist

.. autoclass:: ChecklistQuery

A ChecklistQuery object for fetching checklist records.

Usage
#####

.. code-block:: python

    from pyobis.checklist import ChecklistQuery

    query = ChecklistQuery()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: ChecklistQuery.list
.. automethod:: ChecklistQuery.redlist
.. automethod:: ChecklistQuery.newest
.. automethod:: ChecklistQuery.get_search_url
