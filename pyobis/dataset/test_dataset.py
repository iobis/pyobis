"""Tests for dataset module"""

import pytest
import requests

from pyobis import dataset


@pytest.mark.vcr()
def test_dataset_get_data():
    "dataset.get - test data"
    query = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")
    assert not query.data
    query.execute()
    assert query.data.__class__.__name__ == "dict"
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


@pytest.mark.vcr()
def test_dataset_get_url():
    query = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")
    assert requests.get(query.api_url).status_code == 200
    assert requests.get(query.mapper_url).status_code == 200


@pytest.mark.vcr()
def test_dataset_search_data():
    "dataset.search - test for data"
    query = dataset.search(scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


def test_dataset_get_without_cache():
    "dataset.get - test without cache"
    res = dataset.get("ec9df3b9-3b2b-4d83-881b-27bcbcd57b95", cache=False).execute()
    assert dict == res.__class__
    assert 2 == len(res)
    assert list == res["results"].__class__


@pytest.mark.vcr()
def test_dataset_search_url():
    query = dataset.search(scientificname="Mola mola")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_cache_parameter_functionality():
    """
    Test that the cache parameter in dataset.search and dataset.get works as expected
    without making real HTTP requests.
    """
    res_with_cache = dataset.search(scientificname="Mola mola", cache=True)
    res_without_cache = dataset.search(scientificname="Mola mola", cache=False)

    assert res_with_cache is not None
    assert res_without_cache is not None
    assert not res_with_cache.data
    assert not res_without_cache.data

    dataset_id = "ec9df3b9-3b2b-4d83-881b-27bcbcd57b95"
    get_with_cache = dataset.get(dataset_id, cache=True)
    get_without_cache = dataset.get(dataset_id, cache=False)

    assert get_with_cache is not None
    assert get_without_cache is not None
    assert not get_with_cache.data
    assert not get_without_cache.data
