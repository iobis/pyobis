"""Tests for occurrences module - search methods"""
import os
from pyobis import occurrences

def test_search():
    "occurrences.search - basic test"
    res = occurrences.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__
