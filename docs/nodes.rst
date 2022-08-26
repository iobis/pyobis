.. _nodes:

nodes module
============

.. py:module:: pyobis.nodes

.. autoclass:: OBISQueryResult

An OBISQueryResult object for fetching nodes records.

Usage
#####

.. code-block:: python

    from pyobis.nodes import OBISQueryResult as OQR

    query = OQR()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: OBISQueryResult.search
.. automethod:: OBISQueryResult.activities
.. automethod:: OBISQueryResult.get_search_url
.. automethod:: OBISQueryResult.get_mapper_url
