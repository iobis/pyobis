"""Tests for occurrences module methods"""

import pytest
import requests

from pyobis import occurrences


@pytest.mark.vcr()
def test_occurrences_search():
    """
    occurrences.search - basic test for data, check type, size and other methods
    """
    size = 10100
    query = occurrences.search(scientificname="Mola mola", size=size)
    assert not query.data  # the data is none after query building but before executing
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert size == len(query.to_pandas())
    assert "Mola mola" == query.to_pandas().scientificName[0]


@pytest.mark.vcr()
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
    assert "Abra alba" == query.to_pandas().scientificName[0]
    assert requests.get(query.api_url).status_code == 200
    assert requests.get(query.mapper_url).status_code == 200


@pytest.mark.vcr()
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

    assert isinstance(q1, type(q2))


@pytest.mark.vcr()
def test_occurrences_get():
    """
    occurrences.get - basic test for data, check type, size and other methods
    """
    query = occurrences.get(id=occurrences.search(size=1).execute()["id"].values[0])
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 2 == len(query.data)
    assert list == list(query.data.keys()).__class__
    assert requests.get(query.api_url).status_code == 200
    assert query.to_pandas().__class__.__name__ == "DataFrame"


@pytest.mark.vcr()
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

    # check for KML formats that to_pandas function is not implemented
    with pytest.raises(
        NotImplementedError,
        match="to_pandas method is not yet available for these query types.",
    ):
        query.to_pandas()


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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

    # check for MVT formats that to_pandas function is not implemented
    with pytest.raises(
        NotImplementedError,
        match="to_pandas method is not yet available for these query types.",
    ):
        query.to_pandas()

    query = occurrences.tile(x=1.77, y=52.26, z=0.5, mvt=0, scientificname="Mola mola")
    query.execute()
    assert requests.get(query.api_url).status_code == 200
    assert not query.mapper_url


@pytest.mark.vcr()
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
