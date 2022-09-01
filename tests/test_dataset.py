"""Tests for dataset module"""
import requests

from pyobis.dataset import DatasetQuery as DQR

dataset = DQR()


def test_dataset_get():
    "dataset.get - basic test"
    res = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert requests.get(dataset.get_search_url()).status_code == 200
    assert requests.get(dataset.get_mapper_url()).status_code == 200


def test_dataset():
    "dataset.search - basic test"
    res = dataset.search(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert dataset.get_mapper_url() == "An OBIS mapper URL doesnot exist for this query"
