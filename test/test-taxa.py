"""Tests for taxa module - search methods"""
import os
from pyobis import taxa

def test_search():
    "taxa.search - basic test"
    res = taxa.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__
