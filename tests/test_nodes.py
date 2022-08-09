"""Tests for nodes module"""
from pyobis import nodes


def test_nodes():
    "nodes.search - basic test"
    res = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert str == str(res["results"][0]["description"]).__class__
    assert str == res["results"][0]["id"].__class__


def test_nodes_activities():
    "nodes.activities - basic test"
    res = nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert str == str(res["results"][0]["description"]).__class__
    assert str == res["results"][0]["id"].__class__
