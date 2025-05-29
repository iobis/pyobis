"""Tests for taxa module - search methods"""

import pytest
import requests

from pyobis import taxa


@pytest.mark.vcr()
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


@pytest.mark.vcr()
def test_taxa_search_url():
    """
    taxa.search - basic test for url, url are accessible and
    mapper_url is None for unsupported methods
    """
    query = taxa.search(scientificname="Mola mola")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


@pytest.mark.vcr()
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


@pytest.mark.vcr()
def test_taxa_taxon_url():
    """
    taxa.taxon - basic test for url, url are accessible and
    mapper_url is None for unsupported methods
    """
    query = taxa.taxon(545439)
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


@pytest.mark.vcr()
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


@pytest.mark.vcr()
def test_taxa_annotations_url():
    """
    taxa.annotations - basic test for url, url are accessible and
    mapper_url is None for unsupported methods
    """
    query = taxa.annotations(scientificname="Abra")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_cache_parameter_functionality():
    """
    Test that cache=False parameter works without making actual HTTP requests
    This test verifies the parameter is accepted and handled correctly
    """
    query_with_cache = taxa.search(scientificname="Mola mola", cache=True)
    query_without_cache = taxa.search(scientificname="Mola mola", cache=False)

    assert query_with_cache is not None
    assert query_without_cache is not None
    assert not query_with_cache.data
    assert not query_without_cache.data

    query_taxon_cache = taxa.taxon(545439, cache=True)
    query_taxon_no_cache = taxa.taxon(545439, cache=False)
    assert query_taxon_cache is not None
    assert query_taxon_no_cache is not None

    query_annotations_cache = taxa.annotations(scientificname="Abra", cache=True)
    query_annotations_no_cache = taxa.annotations(scientificname="Abra", cache=False)
    assert query_annotations_cache is not None
    assert query_annotations_no_cache is not None
