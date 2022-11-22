.. _checklist:

checklist module
================

.. py:module:: pyobis.checklist

.. autoclass:: ChecklistResponse

Usage
#####

.. code-block:: python

    from pyobis import checklist

    query = checklist.list(taxonid=127405, **kwargs)
    query.api_url  # Returns the API URL
    query.to_pandas()  # Returns a pandas DataFrame object

Methods:
########

.. autofunction:: list
.. autofunction:: redlist
.. autofunction:: newest
