# pyobis

[![pypi](https://img.shields.io/pypi/v/pyobis.svg)](https://pypi.python.org/pypi/pyobis)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pyobis.svg)](https://anaconda.org/conda-forge/pyobis)
[![docs](https://github.com/iobis/pyobis/actions/workflows/deploy-docs.yml/badge.svg)](https://iobis.github.ic/pyobis)
[![tests](https://github.com/iobis/pyobis/actions/workflows/tests.yml/badge.svg)](https://github.com/iobis/pyobis/actions/workflows/tests.yml)

Python client for the `OBIS API(https://api.obis.org/).

[Source on GitHub at iobis/pyobis](https://github.com/iobis/pyobis)

## What is it?
Pyobis is an interesting python package that helps users fetch data from OBIS API which
harvests occurrence records from thousands of datasets and makes them available as a
single integrated dataset.

[The Ocean Biodiversity Information System (OBIS)](https://obis.org) is a global open-access data and
information clearing-house on marine biodiversity for science, conservation, and sustainable
development, maintained by IOOS.

Other OBIS clients:

+ R: `robis`, [iobis/robis](https://github.com/iobis/robis)

## Main Features
Here are just a few of things pyOBIS can do:

+ Easy handling of OBIS data, easy fetching without handling the raw API response directly.
+ Built-in functions for `occurrence`, `taxon`, `node`, `checklist` and `dataset` endpoints of OBIS API.
+ Provides easy export of data to `Pandas` DataFrame, and helps researchers focus more on analysis rather than data mining.

For examples of how to use this repo, see the jupyter notebooks in the `/notebooks/` directory.
NOTE: GitHub's jupyter notebook display does not show interactive plots; open the notebooks in a jupyter hub (eg colab, binder, etc) for the full experience.

## Installation

### Install from PyPI

```bash
pip install pyobis
```
### Install from conda-forge

Installing pyobis from the conda-forge channel can be achieved by adding conda-forge to your channels with:

```bash
conda install pyobis --channel conda-forge
```
[More information here](https://github.com/conda-forge/pyobis-feedstock)

### Install latest development version from GitHub


```bash
pip install git+git://github.com/iobis/pyobis.git#egg=pyobis
```

Install editable dev version from github for local development. System prerequisites: python3, conda

```bash
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
```

## Documentation

The official documentation is hosted on GitHub Pages [https://iobis.github.io/pyobis](https://iobis.github.io/pyobis).

## Library API

`pyobis` is split up into modules for each of the groups of API methods.

+ `checklist` - Checklist. Generate a checklist of species under a taxa, IUCN Red List, or most recently added species.
+ `dataset` - Dataset. Get metadata of datasets (including `datasetid`, `owner`, `institution`, `number of records`, etc) for a queried spatiotemporal region or taxa.
+ `nodes` - Nodes. Get records or activities for an OBIS node.
+ `occurrences` - Occurrence. Fetch occurrence records, geopoints, lookup for a `scientificname`, extensions (e.g. DNADerivedData, MeasurementOrFacts, etc.)
+ `taxa` - Taxonomic names. Get taxon records with `taxonid` or `scientificname`, and scientific name annotations by the WoRMS team.

You can import the entire library, or each module individually as needed.

## Usage Guide

For a detailed usage guide with information about inputs, output and module functions please read the [Usage Guide](notebooks/usage_guide.ipynb)

## Sample analysis

Some Jupyter Notebook based sample analysis and visualization of data grabbed through `pyobis` have been made available through `/notebooks/` directory.
To get full experience of the interactive plots (eg. geoplots, etc) please open notebooks in a Jupyter Hub (eg. through Google Colab, Binder, local installation, etc.)

## Meta

* License: MIT, see [LICENSE file](LICENSE)
* Help make this project even more useful! Please read the [Contributing Guide](CONTRIBUTING.md).
* Please note that this project is released with a [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms.

## Further Reading

* In case you face data quality issues, please look at [OBIS QC repo](https://github.com/iobis/obis-qc)
* For issues with the package itself, feel free to open an issue here!
