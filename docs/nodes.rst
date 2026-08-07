.. _nodes:

nodes module
============

.. py:module:: pyobis.nodes

.. autoclass:: NodesResponse

Usage
#####

.. code-block:: python

    from pyobis import nodes

    query = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc", cache=True)
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL

Methods:
########

.. autofunction:: search
.. autofunction:: activities
