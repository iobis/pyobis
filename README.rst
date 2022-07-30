******
pyobis
******

|pypi| |docs| |tests|

Python client for the `OBIS API <https://api.obis.org/>`__.

`Source on GitHub at iobis/pyobis <https://github.com/iobis/pyobis>`__

What is it?
===========
Pyobis is an interesting python package that helps users fetch data from OBIS API which
holds a great amount of ocean open-data, with ease.

`The Ocean Biodiversity Information System (OBIS), <https://obis.org>`__ a global open-access data and
information clearing-house on marine biodiversity for science, conservation, and sustainable
development, maintained by IOOS, harvests occurrence records from thousands of datasets
and makes them available as a single integrated dataset via various services including the
OBIS API.

Other OBIS clients:

* R: `robis`, `iobis/robis <https://github.com/iobis/robis>`__

Main Features
=============
Here are just a few of things pyOBIS can do:

* Easy handling of OBIS data, easy fetching without handling the raw API response directly.
* Built-in functions for ``occurrence``, ``taxon``, ``node``, ``checklist`` and ``dataset`` endpoints of OBIS API. 
* Provides easy export of data to ``Pandas`` DataFrame, and helps researchers focus more on analysis rather than data mining.

For examples of how to use this repo, see the jupyter notebooks in the ``/notebooks/`` directory.
NOTE: GitHub's jupyter notebook display does not show interactive plots; open the notebooks in a jupyter hub (eg colab, binder, etc) for the full experience.

Installation
============

Install from pypi

.. code-block:: console

    pip install pyobis

Install latest dev version from github

.. code-block:: console

    pip install git+git://github.com/iobis/pyobis.git#egg=pyobis

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
    # test and generate a coverage report
    python -m pytest -rxs --cov=pyobis tests

Documentation
=============
The official documentation is hosted at readthedocs.io `https://pyobis.readthedocs.io/en/latest/ <https://pyobis.readthedocs.io/en/latest/>`__

Library API
===========

``pyobis`` is split up into modules for each of the groups of API methods.

* ``taxa`` - Taxonomic names
* ``occurrences`` - Occurrence search
* ``dataset`` - Dataset
* ``nodes`` - Nodes
* ``checklist`` - Checklist

You can import the entire library, or each module individually as needed.

Taxa module
###########

.. code-block:: python

    from pyobis import taxa
    taxa.search(scientificname = "Mola mola")
    taxa.search(scientificname = "Mola mola", offset=10)
    taxa.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))')
    taxa.taxon(10332)
    taxa.taxon(127405)

Occurrence module
#################

.. code-block:: python

    from pyobis import occurrences
    occurrences.search(scientificname = "Mola mola")
    occurrences.search(scientificname = "Mola mola", offset=0, size=10)
    occurrences.search(geometry="POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))", size=20)

Dataset module
##############

.. code-block:: python

    from pyobis import dataset
    dataset.search(scientificname = ["Mola", "Abra", "Lanice", "Pectinaria"])
    dataset.get(id = "ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")

Nodes module
############

.. code-block:: python

    from pyobis import nodes
    nodes.search(scientificname = ["Mola", "Abra"] )

Checklist module
################

.. code-block:: python

    from pyobis import checklist as ch
    ch.list(scientificname = "Cetacea")

Usage Guide
===========

For a detailed usage guide with information about inputs, output and module functions please read the `Usage Guide <notebooks/usage_guide.ipynb>`__

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`__
* Help make this project even more useful! Please read the `Contributing Guide <CONTRIBUTING.md>`__.
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`__. By participating in this project you agree to abide by its terms.

Further Reading
===============

* In case you face data quality issues, please look at `OBIS QC repo <https://github.com/iobis/obis-qc>`__
* For issues with the package itself, feel free to open an issue here!

.. |pypi| image:: https://img.shields.io/pypi/v/pyobis.svg
   :target: https://pypi.python.org/pypi/pyobis

.. |docs| image:: https://readthedocs.org/projects/pyobis/badge/?version=latest
   :target: http://pyobis.readthedocs.org/en/latest/?badge=latest

.. |tests| image:: https://github.com/iobis/pyobis/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/iobis/pyobis/actions/workflows/tests.yml   
