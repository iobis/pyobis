"""Tests for nodes module"""

import pytest
import requests

from pyobis import nodes


@pytest.mark.vcr()
def test_nodes_search_data():
    """
    nodes.search - test for data, check type, size and other methods
    """
    query = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert str == str(query.data["results"][0]["description"]).__class__
    assert str == query.data["results"][0]["id"].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


@pytest.mark.vcr()
def test_nodes_search_url():
    """
    nodes.activities - basic test for url, url are accessible and
    mapper_url correct for supported methods
    """
    query = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert requests.get(query.api_url).status_code == 200
    assert requests.get(query.mapper_url).status_code == 200


@pytest.mark.vcr()
def test_nodes_activities_data():
    """
    nodes.activities - basic test for data, check type, size and other methods
    """
    query = nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert str == str(query.data["results"][0]["description"]).__class__
    assert str == query.data["results"][0]["id"].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


@pytest.mark.vcr()
def test_nodes_activities_url():
    """
    nodes.activities - basic test for url, url are accessible and
    mapper_url correct for supported methods
    """
    query = nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_cache_parameter_functionality():
    """
    Test that cache=False parameter works without making actual HTTP requests
    This test verifies the parameter is accepted and handled correctly
    """
    query_with_cache = nodes.search(
        id="4bf79a01-65a9-4db6-b37b-18434f26ddfc",
        cache=True,
    )
    query_without_cache = nodes.search(
        id="4bf79a01-65a9-4db6-b37b-18434f26ddfc",
        cache=False,
    )

    assert query_with_cache is not None
    assert query_without_cache is not None
    assert not query_with_cache.data
    assert not query_without_cache.data

    query_activities_cache = nodes.activities(
        id="4bf79a01-65a9-4db6-b37b-18434f26ddfc",
        cache=True,
    )
    query_activities_no_cache = nodes.activities(
        id="4bf79a01-65a9-4db6-b37b-18434f26ddfc",
        cache=False,
    )
    assert query_activities_cache is not None
    assert query_activities_no_cache is not None
    assert not query_activities_cache.data
    assert not query_activities_no_cache.data
