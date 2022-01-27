"""Tests for taxa module - search methods"""
import os
from pyobis import taxa

def test_taxa_search():
    "taxa.search - basic test"
    res = taxa.search(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__

def test_taxa_taxon():
    "taxa.taxon - basic test"
    res = taxa.taxon(545439)
    assert dict == res.__class__
    assert 15 == len(res)
    assert list == list(res.keys()).__class__
    assert 545439 == res['valid_id']

def test_taxa_taxon():
    "taxa.taxon_search - basic test"
    res = taxa.taxon_search(scientificname = 'Mola')
    assert dict == res.__class__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__
    assert 'Mola' == res['results'][0]['genus']

def test_taxa_common():
    "taxa.common - basic test"
    res = taxa.common(402913)
    assert dict == res.__class__
    assert 5 == len(res)
    assert list == list(res.keys()).__class__
    assert list == res['results'].__class__
    assert dict == res['results'][0].__class__
    xx = list(res['results'][0].keys())
    xx.sort()
    assert ['language', 'name'] == xx
