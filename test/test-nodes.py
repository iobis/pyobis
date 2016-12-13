"""Tests for nodes module"""
import os
from pyobis import nodes

def test_nodes():
    "nodes.node - basic test"
    res = nodes.node(limit = 3)
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert dict == res['results'][0].__class__
    assert str == str(res['results'][0]['description']).__class__
    assert int == res['results'][0]['id'].__class__

