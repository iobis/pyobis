"""Tests for taxa module - search methods"""
import requests

from pyobis import taxa


def test_taxa_search_data():
    """
    taxa.search - basic test for data, check type, size and other methods
    """
    query = taxa.search(scientificname="Mola mola")
    assert not query.data  # the data is none after query building but before executing
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert list == list(query.data.keys()).__class__
    assert 2 == len(query.data)


def test_taxa_search_url():
    """
    taxa.search - basic test for url, url are accessible and
    mapper_url is None for unsupported methods
    """
    query = taxa.search(scientificname="Mola mola")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_taxa_taxon_data():
    """
    taxa.taxon - basic test for data, check type, size and other methods
    """
    query = taxa.taxon(545439)
    assert not query.data
    query.execute()
    assert dict == query.data.__class__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert 545439 == query.data["results"][0]["taxonID"]
    assert query.to_pandas().__class__.__name__ == "DataFrame"


def test_taxa_taxon_url():
    """
    taxa.taxon - basic test for url, url are accessible and
    mapper_url is None for unsupported methods
    """
    query = taxa.taxon(545439)
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_taxa_annotations_data():
    """
    taxa.annotations - basic test for data, check type, size and other methods
    """
    query = taxa.annotations(scientificname="Abra")
    assert not query.data
    query.execute()
    assert dict == query.data.__class__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


def test_taxa_annotations_url():
    """
    taxa.annotations - basic test for url, url are accessible and
    mapper_url is None for unsupported methods
    """
    query = taxa.annotations(scientificname="Abra")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url
