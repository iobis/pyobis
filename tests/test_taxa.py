"""Tests for taxa module - search methods"""
import os

from pyobis import taxa


def test_taxa_search():
    "taxa.search - basic test"
    res = taxa.search(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert list == list(res.keys()).__class__
    assert 2 == len(res)


def test_taxa_taxon():
    "taxa.taxon - basic test"
    res = taxa.taxon(545439)
    assert dict == res.__class__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
    assert 545439 == res["results"][0]["taxonID"]


def test_taxa_annotations():
    "taxa.annotations - basic test"
    res = taxa.annotations(scientificname="Abra")
    assert dict == res.__class__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
