.. _occurrences:

occurrences module
==================

.. py:module:: pyobis.occurrences

.. autoclass:: OccQuery

An OccQuery object for fetching occurrence records.

Usage
#####

.. code-block:: python

    from pyobis.occurrences import OccQuery

    query = OccQuery()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: OccQuery.search
.. automethod:: OccQuery.get
.. automethod:: OccQuery.grid
.. automethod:: OccQuery.getpoints
.. automethod:: OccQuery.point
.. automethod:: OccQuery.tile
.. automethod:: OccQuery.centroid
.. automethod:: OccQuery.get_search_url
.. automethod:: OccQuery.get_mapper_url
.. automethod:: OccQuery.lookup_taxon
