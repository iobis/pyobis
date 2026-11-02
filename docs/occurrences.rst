.. _occurrences:

occurrences module
==================

.. py:module:: pyobis.occurrences

.. autoclass:: OccResponse

Usage
#####

.. code-block:: python

    from pyobis import occurrences

    # Use the Query Builder
    query = occurrences.search(scientificname="Mola mola", cache=True)
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the OBIS API URL
    query.mapper_url  # Returns the OBIS Mapper URL

    # Maximally simple example:
    data = occurrences.search(scientificname="Mola mola").execute()

    # Another example with a bounding box and size limit.
    data = occurrences.search(
        geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))", size=20
    ).execute()

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
