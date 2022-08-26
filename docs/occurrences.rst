.. _occurrences:

occurrences module
==================

.. py:module:: pyobis.occurrences

.. autoclass:: OBISQueryResult

An OBISQueryResult object for fetching occurrence records.

Usage
#####

.. code-block:: python

    from pyobis.occurrences import OBISQueryResult as OQR

    query = OQR()
    data = query.search(args, **kwargs)
    api_url = query.get_query_url()

Methods:
########

.. automethod:: OBISQueryResult.search
.. automethod:: OBISQueryResult.get
.. automethod:: OBISQueryResult.grid
.. automethod:: OBISQueryResult.getpoints
.. automethod:: OBISQueryResult.point
.. automethod:: OBISQueryResult.tile
.. automethod:: OBISQueryResult.centroid
.. automethod:: OBISQueryResult.get_search_url
.. automethod:: OBISQueryResult.get_mapper_url
