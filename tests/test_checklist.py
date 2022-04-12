"""Tests for checklist module"""
import os
from pyobis import checklist as ch

def test_checklist():
    "checklist.list - basic test"
    res = ch.list(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res['results'][0].__class__
    assert int == res['results'][0]['id'].__class__
    assert 'Mola mola' == res['results'][0]['species']

def test_checklist_redlist():
    "checklist.redlist - basic test"
    res = ch.redlist(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res['results'][0].__class__
    assert int == res['results'][0]['id'].__class__
    assert 'Mola mola' == res['results'][0]['species']

def test_checklist_newest():
    "checklist.newest - basic test"
    res = ch.newest(scientificname = 'Mola mola')
    assert 'dict' == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res['results'][0].__class__
    assert int == res['results'][0]['id'].__class__
    assert 'Mola mola' == res['results'][0]['species']