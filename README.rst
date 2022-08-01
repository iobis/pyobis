pyobis
======

|pypi| |docs| |tests|

Python client for the `OBIS API
<https://api.obis.org/>`__.

`Source on GitHub at iobis/pyobis <https://github.com/iobis/pyobis>`__

For examples of how to use this repo, see the jupyter notebooks in the `/notebooks/` directory.
NOTE: GitHub's jupyter notebook display does not show interactive plots; open the notebooks in a jupyter hub (eg colab, binder, etc) for the full experience.

Other OBIS clients:

* R: `robis`, `iobis/robis <https://github.com/iobis/robis>`__

Installation
============

Install from pypi

.. code-block:: console

    pip install pyobis

Install latest dev version from github

.. code-block:: console

    pip install git+git://github.com/sckott/pyobis.git#egg=pyobis

Install editable dev version from github for local development. System prerequisites: python3, conda

.. code-block:: console

    # fetch code
    git clone git@github.com:iobis/pyobis.git
    cd pyobis
    # install
    python -m pip install -r requirements.txt
    python -m pip install -r requirements-dev.txt
    python -m pip install -e .
    # test your installation
    python -m pytest

Library API
===========

`pyobis` is split up into modules for each of the groups of API methods.

* `taxa` - Taxonomic names
* `occurrences` - Occurrence search
* `dataset` - Dataset
* `nodes` - Nodes
* `checklist` - Checklist

You can import the entire library, or each module individually as needed.

Taxa module
===========

.. code-block:: python

    from pyobis import taxa

    taxa.search(scientificname="Mola mola")
    taxa.search(scientificname="Mola mola", offset=10, limit=10)
    taxa.search(
        geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))", limit=20
    )
    taxa.search(aphiaid=key, year="2013", limit=20)
    taxa.taxon(406296)
    taxa.taxon(415282)

Occurrence module
=================

Search

.. code-block:: python

    from pyobis import occurrences

    occurrences.search(scientificname="Mola mola")
    occurrences.search(scientificname="Mola mola", offset=0, limit=10)
    occurrences.search(
        geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))", limit=20
    )
    occurrences.search(aphiaid=key, year="2013", limit=20)

Download

.. code-block:: python

    res = occ.download(year=2001, scientificname="Orcinus")
    res.uuid
    res.status()
    res.fetch()

Dataset module
================

.. code-block:: python

    from pyobis import dataset

    dataset.search(scientificname=["Mola", "Abra", "Lanice", "Pectinaria"])
    dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")

Nodes module
===========

.. code-block:: python

    from pyobis import nodes

    nodes.search(scientificname=["Mola", "Abra"])

Checklist module
================

.. code-block:: python

    from pyobis import checklist as ch

    ch.list(year=2005, scientificname="Cetacea")

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`__
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`__. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/pyobis.svg
   :target: https://pypi.python.org/pypi/pyobis

.. |docs| image:: https://readthedocs.org/projects/pyobis/badge/?version=latest
   :target: http://pyobis.readthedocs.org/en/latest/?badge=latest

.. |tests| image:: https://github.com/iobis/pyobis/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/iobis/pyobis/actions/workflows/tests.yml
