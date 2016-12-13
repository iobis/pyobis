pyobis
======

|docs| |travis| |coverage|

Python client for the `OBIS API
<https://github.com/iobis/api-docs>`__.

`Source on GitHub at sckott/pyobis <https://github.com/sckott/pyobis>`__

Other OBIS clients:

* R: `robis`, `iobis/robis <https://github.com/iobis/robis>`__

Installation
============

from pypi

.. code-block:: console

    pip install pyobis

dev version

.. code-block:: console

    pip install git+git://github.com/sckott/pyobis.git#egg=pyobis


library API
===========

`pyobis` is split up into modules for each of the groups of API methods.

* `taxa` - Taxonomic names
* `occurrences` - Occurrence search, and occurrence downloads
* `resources` - Resources
* `groups` - Groups
* `nodes` - Nodes
* `checklist` - Checklist

You can import the entire library, or each module individually as needed.

Taxa module
===========

.. code-block:: python

    from pyobis import taxa
    taxa.search(scientificname = 'Mola mola')
    taxa.search(scientificname = 'Mola mola', offset=10, limit=10)
    taxa.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
    taxa.search(aphiaid=key, year="2013", limit=20)
    taxa.taxon(406296)
    taxa.taxon(415282)

Occurrence module
=================

Search

.. code-block:: python

    from pyobis import occurrences
    occurrences.search(scientificname = 'Mola mola')
    occurrences.search(scientificname = 'Mola mola', offset=0, limit=10)
    occurrences.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
    occurrences.search(aphiaid=key, year="2013", limit=20)

Download

.. code-block:: python

    res = occ.download(year = 2001, scientificname = 'Orcinus')
    res.uuid
    res.status()
    res.fetch()

Resources module
================

.. code-block:: python

    from pyobis import resources
    resources.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])
    resources.resource(103)
    resources.citation(scientificname = 'Mola mola')

Groups module
=============

.. code-block:: python

    from pyobis import groups
    groups.group()
    groups.group(limit = 3)

Ndes module
===========

.. code-block:: python

    from pyobis import nodes
    nodes.node()

Checklist module
================

.. code-block:: python

    from pyobis import checklist as ch
    ch.list(year = 2005, scientificname = 'Cetacea')

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`__
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`__. By participating in this project you agree to abide by its terms.

.. |docs| image:: https://readthedocs.org/projects/pyobis/badge/?version=latest
   :target: http://pyobis.readthedocs.org/en/latest/?badge=latest

.. |travis| image:: https://travis-ci.org/sckott/pyobis.svg
   :target: https://travis-ci.org/sckott/pyobis

.. |coverage| image:: https://coveralls.io/repos/sckott/pyobis/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/pyobis?branch=master
