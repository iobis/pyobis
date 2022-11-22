pyobis
======

|pypi| |docs|

Python client for the `OBIS API
<https://api.obis.org/>`__.

`Source on GitHub at iobis/pyobis <https://github.com/iobis/pyobis>`__

Other OBIS clients:

* R: `robis`, `iobis/robis <https://github.com/iobis/robis>`__

Installation
============

from pypi

.. code-block:: console

    pip install pyobis

dev version

.. code-block:: console

    pip install git+git://github.com/iobis/pyobis.git#egg=pyobis


Library API
===========

``pyobis`` is split up into modules for each of the groups of API methods.

* ``checklist`` - Checklist. Generate a checklist of species under a taxa, IUCN Red List, or most recently added species.
* ``dataset`` - Dataset. Get metadata of datasets (including ``datasetid``, ``owner``, ``institution``, ``number of records``, etc) for a queried spatiotemporal region or taxa.
* ``nodes`` - Nodes. Get records or activities for an OBIS node.
* ``occurrences`` - Occurrence. Fetch occurrence records, geopoints, lookup for a ``scientificname``, extensions (e.g. DNADerivedData, MeasurementOrFacts, etc.)
* ``taxa`` - Taxonomic names. Get taxon records with ``taxonid`` or ``scientificname``, and scientific name annotations by the WoRMS team.

You can import the entire library, or each module individually as needed.

Taxa module
###########

.. code-block:: python

    from pyobis import taxa

    query = taxa.search(scientificname="Mola mola")
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL

    data = taxa.search(scientificname="Mola mola").execute()
    taxa.search(geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))")
    taxa.taxon(10332)
    taxa.taxon(127405)


Occurrence module
#################

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


Dataset module
##############

.. code-block:: python

    from pyobis import dataset

    query = dataset.search(scientificname=["Mola", "Abra", "Lanice", "Pectinaria"])
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL

    data = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95").execute()

Nodes module
############

.. code-block:: python

    from pyobis import nodes

    query = nodes.search(scientificname=["Mola", "Abra"])
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL

Checklist module
################

.. code-block:: python

    from pyobis import checklist

    query = checklist.list(scientificname="Cetacea")
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the OBIS API URL

Meta
====

* License: MIT, see `LICENSE file <https://github.com/iobis/pyobis/blob/master/LICENSE>`__
* Please note that this project is released with a `Contributor Code of Conduct <https://github.com/iobis/pyobis/blob/master/CONDUCT.md>`__. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/pyobis.svg
   :target: https://pypi.python.org/pypi/pyobis

.. |docs| image:: https://github.com/iobis/pyobis/actions/workflows/deploy-docs.yml/badge.svg
   :target: https://iobis.github.io/pyobis



Contents
========

.. toctree::
   :maxdepth: 2

   occurrences
   taxa
   dataset
   nodes
   checklist
   changelog_link

License
=======

MIT


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
