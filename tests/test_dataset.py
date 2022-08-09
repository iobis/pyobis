"""Tests for dataset module"""
from pyobis import dataset


def test_dataset_get():
    "dataset.get - basic test"
    res = dataset.get(id="ec9df3b9-3b2b-4d83-881b-27bcbcd57b95")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__


def test_dataset():
    "dataset.search - basic test"
    res = dataset.search(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
