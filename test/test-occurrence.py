"""Tests for occurrences module - search methods"""
import os
from pyobis import occurrences as occ

def test_occurrences_search():
    "occurrences.search - basic test"
    res = occ.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__

def test_occurrences_search_limit():
    "occurrences.search - limit param works"
    res = occ.search(scientificname = 'Mola mola', limit=3)
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert 3 == len(res['results'])
