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
    "dataset.get - test data"
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


@pytest.mark.vcr()
def test_dataset_search_url():
    "dataset.search - test for data"
    query = dataset.search(scientificname="Mola mola")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


@pytest.mark.vcr()
def test_dataset_search_keywords():
    "dataset search with keywords"
    query = dataset.search(keyword="coral")
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


@pytest.mark.vcr()
def test_cache_parameter_functionality():
    """
    dataset.search, dataset.get - test cache parameter functionality
    """
    res_with_cache = dataset.search(scientificname="Mola mola", cache=True)
    res_without_cache = dataset.search(scientificname="Mola mola", cache=False)

    assert res_with_cache is not None
    assert res_without_cache is not None
    assert not res_with_cache.data
    assert not res_without_cache.data

    # post-execution state
    res_with_cache.execute()
    res_without_cache.execute()
    assert res_with_cache.data is not None
    assert res_without_cache.data is not None
    assert "dict" == res_with_cache.data.__class__.__name__
    assert "dict" == res_without_cache.data.__class__.__name__

    dataset_id = "ec9df3b9-3b2b-4d83-881b-27bcbcd57b95"
    get_with_cache = dataset.get(dataset_id, cache=True)
    get_without_cache = dataset.get(dataset_id, cache=False)

    assert get_with_cache is not None
    assert get_without_cache is not None
    assert not get_with_cache.data
    assert not get_without_cache.data

    # test post-execution state
    get_with_cache.execute()
    get_without_cache.execute()
    assert get_with_cache.data is not None
    assert get_without_cache.data is not None
    assert "dict" == get_with_cache.data.__class__.__name__
    assert "dict" == get_without_cache.data.__class__.__name__
