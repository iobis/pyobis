"""Tests for dataset module"""
import requests

from pyobis import dataset


def test_dataset_get_data():
    "dataset.get - test data"
    query = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")
    assert not query.data
    query.execute()
    assert query.data.__class__.__name__ == "dict"
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


def test_dataset_get_url():
    query = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")
    assert requests.get(query.api_url).status_code == 200
    assert requests.get(query.mapper_url).status_code == 200


def test_dataset_search_data():
    "dataset.search - test for data"
    query = dataset.search(scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert dict == query.data["results"][0].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"


def test_dataset_search_url():
    query = dataset.search(scientificname="Mola mola")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url
