"""Tests for occurrences module methods"""
import requests

from pyobis import occurrences


def test_occurrences_search():
    """
    occurrences.search - basic test for data, check type, size and other methods
    """
    size = 10100
    query = occurrences.search(scientificname="Mola mola", size=size)
    assert not query.data  # the data is none after query building but before executing
    query.execute()
    assert size == len(query.data)
    assert "Mola mola" == query.data.scientificName[0]


def test_occurrence_search_mof():
    """
    occurrences.search - basic test for data with MoF extension, check type, size and other methods
    """
    query = occurrences.search(
        scientificname="Abra alba",
        mof=True,
        size=100,
        hasextensions="MeasurementOrFact",
    )
    assert not query.data
    query.execute()
    assert "Abra alba" == query.data.scientificName[0]
    assert requests.get(query.api_url).status_code == 200
    assert requests.get(query.mapper_url).status_code == 200


def test_occurrences_search_61():
    """
    Search returns same object-type regardless of mof=True or mof=False.
    Tests for https://github.com/iobis/pyobis/issues/61.
    """
    TEST_QUERY = dict(
        scientificname="Mola mola",
        size=2,
    )
    q1 = occurrences.search(mof=True, **TEST_QUERY).execute()
    q2 = occurrences.search(mof=False, **TEST_QUERY).execute()

    assert type(q1) == type(q2)


def test_occurrences_get():
    """
    occurrences.get - basic test for data, check type, size and other methods
    """
    query = occurrences.get(id="00003cf7-f2fc-4c53-98a6-7d846e70f5d1")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert requests.get(query.api_url).status_code == 200
    assert query.to_pandas().__class__.__name__ == "DataFrame"


def test_occurrences_grid():
    """
    occurrences.grid - basic test for data, check type, size and other methods
    """
    query = occurrences.grid(5, geojson=True, scientificname="Abra alba")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    query = occurrences.grid(5, geojson=False, scientificname="Mola mola")
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_occurrences_getpoints():
    """
    occurrences.getpoints - basic test for data, check type, size and other methods
    """
    query = occurrences.getpoints(scientificname=["Mola mola", "Abra alba"])
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_occurrences_point():
    """
    occurrences.point - basic test for data, check type, size and other methods
    """
    query = occurrences.point(x=1.77, y=54.22, scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_occurrences_tile():
    """
    occurrences.tile - basic test for data, check type, size and other methods
    """
    query = occurrences.tile(x=1.77, y=52.26, z=0.5, mvt=0, scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    query = occurrences.tile(x=1.77, y=52.26, z=0.5, mvt=1, scientificname="Mola mola")
    query.execute()
    assert requests.get(query.api_url).status_code == 200
    query = occurrences.tile(x=1.77, y=52.26, z=0.5, mvt=0, scientificname="Mola mola")
    query.execute()
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


def test_occurrences_centroid():
    """
    occurrences.centroid - basic test for data, check type, size and other methods
    """
    query = occurrences.centroid(scientificname="Mola mola")
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url
