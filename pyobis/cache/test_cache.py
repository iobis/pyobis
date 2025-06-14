"""
Unit tests for the cache module.
"""

import os
import shutil
import sys
import tempfile
import time
from datetime import timedelta
from pathlib import Path

import pytest
import requests
import requests_cache

from .cache import Cache, get_default_cache


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    try:
        shutil.rmtree(temp_dir)
    except PermissionError:
        # for windows
        time.sleep(0.1)
        try:
            shutil.rmtree(temp_dir)
        except PermissionError:
            print(f"Warning: Could not delete temporary directory {temp_dir}")


@pytest.fixture
def cache(temp_cache_dir):
    """Create a Cache instance with a temporary directory."""
    cache = Cache(cache_dir=temp_cache_dir, expire_after=1)
    yield cache
    cache.close()


def test_cache_initialization(cache):
    """Test cache initialization."""
    assert os.path.exists(cache.cache_dir)
    assert hasattr(cache, "session")
    assert cache.expire_after == 1


def test_cache_disabled():
    """Test cache initialization with caching disabled."""
    cache = Cache(enabled=False)
    assert not cache.enabled
    assert isinstance(cache.session, requests.Session)
    assert not isinstance(cache.session, requests_cache.CachedSession)
    cache.close()


def test_get_default_cache():
    """Test get_default_cache function."""
    # Test with caching enabled
    cache = get_default_cache(enabled=True)
    assert cache.enabled
    assert isinstance(cache.session, requests_cache.CachedSession)
    cache.close()

    # Test with caching disabled
    cache = get_default_cache(enabled=False)
    assert not cache.enabled
    assert isinstance(cache.session, requests.Session)
    cache.close()


def test_request_caching(cache):
    """Test HTTP request caching."""
    session = cache.get_session()
    session.get("https://api.obis.org/v3/taxon/123")
    response = session.get("https://api.obis.org/v3/taxon/123")
    assert response.from_cache


def test_request_no_caching():
    """Test HTTP requests without caching."""
    cache = Cache(enabled=False)
    session = cache.get_session()
    response1 = session.get("https://api.obis.org/v3/taxon/123")
    response2 = session.get("https://api.obis.org/v3/taxon/123")
    assert not hasattr(response1, "from_cache")
    assert not hasattr(response2, "from_cache")
    cache.close()


def test_cache_expiration(cache):
    """Test cache expiration."""
    session = cache.get_session()
    response1 = session.get("https://api.obis.org/v3/taxon/123")
    assert not response1.from_cache

    response2 = session.get("https://api.obis.org/v3/taxon/123")
    assert response2.from_cache

    time.sleep(2)
    cache.remove_expired()
    response3 = session.get("https://api.obis.org/v3/taxon/123")
    assert not response3.from_cache


def test_cache_clear(cache):
    """Test clearing the cache."""
    session = cache.get_session()
    session.get("https://api.obis.org/v3/taxon/123")

    cache.clear()

    response = session.get("https://api.obis.org/v3/taxon/123")
    assert not response.from_cache


def test_remove_expired(cache):
    """Test removing expired cache entries."""
    session = cache.get_session()
    session.get("https://api.obis.org/v3/taxon/123")

    time.sleep(2)

    cache.remove_expired()

    info = cache.get_cache_info()
    assert info["cache_count"] == 0


def test_get_cache_info(cache):
    """Test getting cache information."""
    session = cache.get_session()
    session.get("https://api.obis.org/v3/taxon/123")
    session.get("https://api.obis.org/v3/taxon/456")

    info = cache.get_cache_info()

    assert "cache_enabled" in info
    assert info["cache_enabled"] is True
    assert "cache_path" in info
    assert "cache_size" in info
    assert "cache_count" in info
    assert "expire_after" in info
    assert isinstance(info["expire_after"], timedelta)
    assert info["expire_after"].total_seconds() == 1
    assert info["cache_count"] == 2


def test_get_cache_info_disabled():
    """Test getting cache information when caching is disabled."""
    cache = Cache(enabled=False)
    info = cache.get_cache_info()

    assert "cache_enabled" in info
    assert info["cache_enabled"] is False
    assert info["cache_path"] is None
    assert info["cache_size"] == 0
    assert info["cache_count"] == 0
    assert info["expire_after"] is None
    cache.close()


def test_context_manager(cache):
    """Test cache as context manager."""
    with Cache(cache_dir=cache.cache_dir) as ctx_cache:
        session = ctx_cache.get_session()
        response = session.get("https://api.obis.org/v3/taxon/123")
        assert response.status_code == 200


def test_cache_directory_location():
    """Test that cache directory is created in the correct platform-specific location."""
    cache = Cache()
    try:
        if sys.platform.startswith("win"):
            expected_base = os.environ.get(
                "LOCALAPPDATA",
                str(Path.home() / "AppData" / "Local"),
            )
        else:
            expected_base = os.environ.get(
                "XDG_CACHE_HOME",
                str(Path.home() / ".cache"),
            )

        expected_path = Path(expected_base) / "pyobis"
        assert cache.cache_dir == expected_path
        assert cache.cache_dir.exists()
    finally:
        cache.close()
