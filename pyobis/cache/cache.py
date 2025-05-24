"""
Cache management module for pyobis.
Handles HTTP request caching using requests-cache with filesystem backend.
"""

import logging
from datetime import timedelta
from pathlib import Path

import requests_cache

logger = logging.getLogger(__name__)


class Cache:
    """
    Cache manager for pyobis using requests-cache.
    Provides HTTP request caching with filesystem backend.
    """

    def __init__(self, cache_dir=None, expire_after=3600):
        """
        Initialize the cache manager.

        Args:
            cache_dir (str, optional): Directory to store cache files.
                                     Defaults to pyobis/cache/requests.
            expire_after (int, optional): Cache expiration time in seconds.
                                        Defaults to 1 hour (3600 seconds).
        """
        self.cache_dir = (
            Path(cache_dir) if cache_dir else Path(__file__).parent / "requests"
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.expire_after = expire_after

        # Configure the cache session
        self.session = requests_cache.CachedSession(
            cache_name=str(self.cache_dir / "obis_cache"),
            backend="filesystem",
            expire_after=timedelta(seconds=expire_after),
            allowable_methods=["GET"],
            stale_if_error=True,
            cache_control=True,
            serializer="json",
            use_cache_dir=True,
            use_temp=True,
        )

        logger.info(f"Cache initialized at {self.cache_dir}")

    def get_session(self):
        """
        Get the cached session for making requests.

        Returns:
            requests_cache.CachedSession: The cached session object.
        """
        return self.session

    def clear(self):
        """Clear all cached responses."""
        self.session.cache.clear()
        logger.info("Cache cleared")

    def remove_expired(self):
        """Remove expired cache entries."""
        self.session.cache.delete(expired=True)
        logger.info("Expired cache entries removed")

    def get_cache_info(self):
        """
        Get information about the cache.

        Returns:
            dict: Cache information including path, size, and count.
        """

        total_size = 0
        for path in self.cache_dir.rglob("*"):
            if path.is_file():
                total_size += path.stat().st_size

        return {
            "cache_path": str(self.cache_dir),
            "cache_size": total_size,
            "cache_count": len(self.session.cache.responses),
            "expire_after": timedelta(seconds=self.expire_after),
        }

    def close(self):
        """Close the session and release all resources."""
        if hasattr(self, "session"):
            self.session.close()
            if hasattr(self.session, "cache"):
                self.session.cache.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


cache = Cache()
