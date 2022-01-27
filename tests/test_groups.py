"""Tests for groups module"""
import os
from pyobis import groups

def test_groups():
    "groups.group - basic test"
    res = groups.group(limit = 3)
    assert 'dict' == res.__class__.__name__
    assert 5 == len(res)
    assert dict == res['results'][0].__class__
    assert int == res['results'][0]['id'].__class__

