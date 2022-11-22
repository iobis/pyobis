.. _nodes:

nodes module
============

.. py:module:: pyobis.nodes

.. autoclass:: NodesResponse

Usage
#####

.. code-block:: python

    from pyobis import nodes

    query = nodes.search(scientificname=["Mola", "Abra"], **kwargs)
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL

Methods:
########

.. autofunction:: search
.. autofunction:: activities
