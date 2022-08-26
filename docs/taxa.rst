.. _taxa:

taxa module
===========

.. py:module:: pyobis.taxa

.. autoclass:: OBISQueryResult

An OBISQueryResult object for fetching taxa records.

Usage
#####

.. code-block:: python

    from pyobis.taxa import OBISQueryResult as OQR

    query = OQR()
    data = query.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: taxa.search
.. automethod:: taxa.taxon
.. automethod:: taxa.annotations
.. automethod:: taxa.get_search_url
