.. _nodes:

nodes module
============

.. py:module:: pyobis

.. autoclass:: OBISQueryResult

An OBISQueryResult object for fetching nodes records.

Usage
#####

.. code-block:: python

    from pyobis.nodes import OBISQueryResult as OQR

    query = OQR()
    data = nodes.search(args, **kwargs)
    api_url = query.get_search_url()

Methods:
########

.. automethod:: OBISQueryResult.search
.. automethod:: OBISQueryResult.activities
