.. _nodes:

nodes module
============

.. py:module:: pyobis.nodes

.. autoclass:: NodesQuery

A NodesQuery object for fetching nodes records.

Usage
#####

.. code-block:: python

    from pyobis.nodes import NodesQuery

    query = NodesQuery()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: NodesQuery.search
.. automethod:: NodesQuery.activities
.. automethod:: NodesQuery.get_search_url
.. automethod:: NodesQuery.get_mapper_url
