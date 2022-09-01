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

* ``taxa`` - Taxonomic names
* ``occurrences`` - Occurrences
* ``dataset`` - Dataset
* ``nodes`` - Nodes
* ``checklist`` - Checklist

You can import the entire library, or each module individually as needed.

Taxa module
###########

.. code-block:: python

    from pyobis.taxa import TaxaQuery

    query = TaxaQuery()

    query.search(scientificname="Mola mola")
    query.search(scientificname="Mola mola", offset=10)
    query.search(geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))")
    query.taxon(10332)
    query.taxon(127405)
    query.get_search_url()

Occurrence module
#################

.. code-block:: python

    from pyobis.occurrences import OccQuery

    query = OccQuery()

    query.search(scientificname="Mola mola")
    query.search(scientificname="Mola mola", offset=0, size=10)
    query.search(
        geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))", size=20
    )
    query.get_mapper_url()

Dataset module
##############

.. code-block:: python

    from pyobis.dataset import DatasetQuery

    query = DatasetQuery()

    query.search(scientificname=["Mola", "Abra", "Lanice", "Pectinaria"])
    query.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")

Nodes module
############

.. code-block:: python

    from pyobis.nodes import NodesQuery

    query = NodesQuery()

    query.search(scientificname=["Mola", "Abra"])
    query.get_search_url()

Checklist module
################

.. code-block:: python

    from pyobis.checklist import ChecklistQuery

    query = ChecklistQuery()

    query.list(scientificname="Cetacea")

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
