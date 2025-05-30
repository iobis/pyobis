"""Tests for checklist module"""

import pytest
import requests

from pyobis import checklist


@pytest.mark.vcr()
def test_checklist():
    """
    checklist.list - basic test for data, check type, size and other methods
    """
    query = checklist.list(scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert int == query.data["results"][0]["taxonID"].__class__
    assert "Mola mola" == query.data["results"][0]["species"]
    assert requests.get(query.api_url).status_code == 200


@pytest.mark.vcr()
def test_checklist_redlist():
    """
    checklist.redlist - basic test for data, check type, size and other methods
    """
    query = checklist.redlist(scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert int == query.data["results"][0]["taxonID"].__class__
    assert "Mola mola" == query.data["results"][0]["species"]
    assert requests.get(query.api_url).status_code == 200


@pytest.mark.vcr()
def test_checklist_newest():
    """
    checklist.newest - basic test for data, check type, size and other methods
    """
    query = checklist.newest(scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 1 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert int == query.data["results"][0]["taxonID"].__class__
    assert "Mola mola" == query.data["results"][0]["species"]
    assert requests.get(query.api_url).status_code == 200
    assert query.to_pandas().__class__.__name__ == "DataFrame"


@pytest.mark.vcr()
def test_cache_parameter_functionality():
    """
    checklist.list - test cache parameter functionality
    """
    query_with_cache = checklist.list(scientificname="Mola mola", cache=True)
    query_without_cache = checklist.list(scientificname="Mola mola", cache=False)

    assert query_with_cache is not None
    assert query_without_cache is not None

    assert not query_with_cache.data
    assert not query_without_cache.data
