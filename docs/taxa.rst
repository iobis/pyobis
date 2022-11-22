.. _taxa:

taxa module
===========

.. py:module:: pyobis.taxa

.. autoclass:: TaxaResponse

Usage
#####

.. code-block:: python

    from pyobis import taxa

    query = taxa.search(scientificname="Mola mola")
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL
    query.to_pandas()  # Returns a pandas DataFrame

    data = taxa.search(scientificname="Mola mola").execute()
    taxa.search(geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))")
    taxa.taxon(10332)
    taxa.taxon(127405)

Methods:
########

.. autofunction:: search
.. autofunction:: taxon
.. autofunction:: annotations
