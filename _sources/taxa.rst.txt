.. _taxa:

taxa module
===========

.. py:module:: pyobis.taxa

.. autoclass:: TaxaQuery

A TaxaQuery object for fetching taxa records.

Usage
#####

.. code-block:: python

    from pyobis.taxa import TaxaQuery

    query = TaxaQuery()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: TaxaQuery.search
.. automethod:: TaxaQuery.taxon
.. automethod:: TaxaQuery.annotations
.. automethod:: TaxaQuery.get_search_url
