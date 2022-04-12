"""Tests for occurrences module - search methods"""
import os
from pyobis import occurrences as occ

def test_occurrences_search():
    "occurrences.search - basic test"
    res = occ.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__

def test_occurrences_get():
    "occurrences.get - basic test"
    res = occ.get(id = 135355)
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__