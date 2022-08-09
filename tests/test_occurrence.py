"""Tests for occurrences module - search methods"""
from pyobis import occurrences as occ


def test_occurrences_search():
    "occurrences.search - basic test"
    res = occ.search(scientificname="Mola mola", size=10100)
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
    res = occ.search(
        scientificname="Abra alba",
        mof=True,
        size=100,
        hasextensions="MeasurementOrFact",
    )
    assert "Abra alba" == res.scientificName[0]


def test_occurrences_get():
    "occurrences.get - basic test"
    res = occ.get(id="00023244-457b-48be-8db1-1334d44d6624")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__


def test_occurrences_grid():
    "occurrences.grid - basic test"
    res = occ.grid(5, geojson=True, scientificname="Abra alba")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
    res = occ.grid(5, geojson=False, scientificname="Mola mola")


def test_occurrences_getpoints():
    "occurrences.getpoints - basic test"
    res = occ.getpoints(scientificname=["Mola mola", "Abra alba"])
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__


def test_occurrences_point():
    "occurrences.point - basic test"
    res = occ.point(x=1.77, y=54.22, scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__


def test_occurrences_tile():
    "occurrences.tile - basic test"
    res = occ.tile(x=1.77, y=52.26, z=0.5, mvt=0, scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
    res = occ.tile(x=1.77, y=52.26, z=0.5, mvt=1, scientificname="Mola mola")


def test_occurrences_centroid():
    "occurrences.centroid - basic test"
    res = occ.centroid(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
