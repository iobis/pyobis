"""Tests for nodes module"""
import requests

from pyobis.nodes import NodesQuery as NQR

nodes = NQR()


def test_nodes():
    "nodes.search - basic test"
    res = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert str == str(res["results"][0]["description"]).__class__
    assert str == res["results"][0]["id"].__class__
    assert requests.get(nodes.get_search_url()).status_code == 200
    assert requests.get(nodes.get_mapper_url()).status_code == 200


def test_nodes_activities():
    "nodes.activities - basic test"
    res = nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert str == str(res["results"][0]["description"]).__class__
    assert str == res["results"][0]["id"].__class__
    assert nodes.get_mapper_url() == "An OBIS mapper URL doesnot exist for this query"
