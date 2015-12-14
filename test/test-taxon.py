"""Tests for taxon module - search methods"""
import os
from pyobis import taxon

def test_search():
    "taxon.search - basic test"
    res = taxon.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__
