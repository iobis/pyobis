"""Tests for checklist module"""
from unittest import TestCase

import requests

from pyobis.checklist import ChecklistQuery as CQR


class Test_ChecklistQueryList(TestCase):
    @classmethod
    def setUpClass(cls):
        "performs one query to run the tests on"
        cls.ch = CQR()
        cls.res = cls.ch.list(scientificname="Mola mola")

    def test_checklist_is_dict(self):
        ".list() returns dict"
        self.assertEqual("dict", self.res.__class__.__name__)

    def test_checklist_dict_len_2(self):
        ".list() returns object w/ len 2"
        self.assertEqual(2, len(self.res))

    def test_checklist_has_results_dict(self):
        ".list()[results] is dict"
        self.assertEqual(dict, self.res["results"][0].__class__)

    def test_checklist_taxonid_is_int(self):
        "first taxonID in result is an integer"
        self.assertEqual(int, self.res["results"][0]["taxonID"].__class__)

    def test_checklist_species_matches_query(self):
        ".list() species in first result is requested species"
        self.assertEqual("Mola mola", self.res["results"][0]["species"])

    def test_checklist_search_url_is_valid(self):
        ".list() result search url responds with status 200"
        self.assertEqual(requests.get(self.ch.get_search_url()).status_code, 200)


def test_checklist_redlist():
    "checklist.redlist - basic test"
    res = CQR().redlist(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert dict == res["results"][0].__class__
    assert int == res["results"][0]["taxonID"].__class__
    assert "Mola mola" == res["results"][0]["species"]


def test_checklist_newest():
    "checklist.newest - basic test"
    res = CQR().newest(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 1 == len(res)
    assert dict == res["results"][0].__class__
    assert int == res["results"][0]["taxonID"].__class__
    assert "Mola mola" == res["results"][0]["species"]
