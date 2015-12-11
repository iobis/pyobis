"""Tests for taxon module - search methods"""
import os
from pyobis import taxon

def test_search():
    "taxon.search - basic test"
    res = taxon.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert [u'count', u'lastpage', u'limit', u'results', u'offset'] == res.keys()
