pyobis
======

|docs| |travis| |coverage|

Python client for the `OBIS API
<https://github.com/iobis/api-docs>`__.

`Source on GitHub at sckott/pyobis <https://github.com/sckott/pyobis>`__

Other OBIS clients:

* R: `obisclient`, `iobis/obisclient <https://github.com/iobis/obisclient>`__

Installation
============

.. code-block:: console

    [sudo] pip install git+git://github.com/sckott/pyobis.git#egg=pyobis

`pyobis` is split up into modules for each of the major groups of API methods.

* Taxa - Taxonomic names
* Occurrences - Occurrence search

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

.. code-block:: python

    from pyobis import occurrences
    occurrences.search(scientificname = 'Mola mola')
    occurrences.search(scientificname = 'Mola mola', offset=0, limit=10)
    occurrences.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
    occurrences.search(aphiaid=key, year="2013", limit=20)

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


Contents
--------

.. toctree::
   :maxdepth: 2

   occurrences
   taxa
   groups
   resources
   changelog_link

License
-------

MIT


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

