"""Tests for resources module"""
import os
from pyobis import resources

def test_resources():
    "resources.search - basic test"
    res = resources.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert dict == res['results'][0].__class__

