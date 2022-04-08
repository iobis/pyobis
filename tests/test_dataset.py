"""Tests for dataset module"""
import os
from pyobis import dataset

def test_getbyid():
    "dataset.get - basic test"
    res = dataset.get(id = 2126)
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res['results'][0].__class__

def test_dataset():
    "dataset.search - basic test"
    res = dataset.search(scientificname='Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res['results'][0].__class__