"""Tests for occurrences module methods"""
import requests

from pyobis.occurrences import OccQuery as OQR

data = OQR()


def test_occurrences_search():
    "occurrences.search - basic test"
    size = 10100
    res = data.search(scientificname="Mola mola", size=size)
    assert size == len(res)
    assert "Mola mola" == res.scientificName[0]
    res = data.search(
        scientificname="Abra alba",
        mof=True,
        size=100,
        hasextensions="MeasurementOrFact",
    )
    assert "Abra alba" == res.scientificName[0]
    assert requests.get(data.get_search_url()).status_code == 200
    assert requests.get(data.get_mapper_url()).status_code == 200


def test_occurrences_search_61():
    """
    Search returns same object-type regardless of mof=True or mof=False.
    Tests for https://github.com/iobis/pyobis/issues/61.
    """
    TEST_QUERY = dict(
        scientificname="Mola mola",
        size=2,
    )
    res1 = data.search(mof=True, **TEST_QUERY)
    res2 = data.search(mof=False, **TEST_QUERY)
    assert type(res1) == type(res2)


def test_occurrences_get():
    "occurrences.get - basic test"
    res = data.get(id="00023244-457b-48be-8db1-1334d44d6624")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__


def test_occurrences_grid():
    "occurrences.grid - basic test"
    res = data.grid(5, geojson=True, scientificname="Abra alba")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
    res = data.grid(5, geojson=False, scientificname="Mola mola")
    assert data.get_mapper_url() == "An OBIS mapper URL doesnot exist for this query"


def test_occurrences_getpoints():
    "occurrences.getpoints - basic test"
    res = data.getpoints(scientificname=["Mola mola", "Abra alba"])
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__


def test_occurrences_point():
    "occurrences.point - basic test"
    res = data.point(x=1.77, y=54.22, scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__


def test_occurrences_tile():
    "occurrences.tile - basic test"
    res = data.tile(x=1.77, y=52.26, z=0.5, mvt=0, scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
    res = data.tile(x=1.77, y=52.26, z=0.5, mvt=1, scientificname="Mola mola")


def test_occurrences_centroid():
    "occurrences.centroid - basic test"
    res = data.centroid(scientificname="Mola mola")
    assert "dict" == res.__class__.__name__
    assert 2 == len(res)
    assert list == list(res.keys()).__class__
