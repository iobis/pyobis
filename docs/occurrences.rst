.. _occurrences:

occurrences module
==================

.. py:module:: pyobis.occurrences

.. autoclass:: OccResponse

Usage
#####

.. code-block:: python

    from pyobis import occurrences

    query = occurrences.search(scientificname="Mola mola")
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the OBIS API URL
    query.mapper_url  # Returns the OBIS Mapper URL

    data = occurrences.search(scientificname="Mola mola", size=10).execute()
    occurrences.search(
        geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))", size=20
    )

Methods:
########

.. autofunction:: search
.. autofunction:: get
.. autofunction:: grid
.. autofunction:: getpoints
.. autofunction:: point
.. autofunction:: tile
.. autofunction:: centroid
.. autofunction:: lookup_taxon
