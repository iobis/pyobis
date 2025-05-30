"""
Utility functions for internal use across various modules.
"""

import logging
from urllib.parse import urlencode

from cache import get_default_cache

obis_baseurl = "https://api.obis.org/v3/"

# export logger, and setup basic configurations
logger = logging.getLogger(__name__)
logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class NoResultException(Exception):
    """
    Thrown when query returns no results.
    """

    pass


def build_api_url(url, args):
    """
    Builds the API URL based on the base url and the arguments
    """
    return url + "?" + urlencode({k: v for k, v in args.items() if v is not None})


def obis_GET(url, args, ctype, cache=True, **kwargs):
    """
    Handles technical details of sending GET request to the API

    Args:
        url (str): The URL to request
        args (dict): Query parameters
        ctype (str): Expected content type
        cache (bool, optional): Whether to use caching. Defaults to True.
        **kwargs: Additional arguments to pass to requests
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "api.obis.org",
        "Connection": "keep-alive",
    }

    # Get a cache instance based on the boolean parameter
    cache_instance = get_default_cache(enabled=cache)
    session = cache_instance.get_session()

    out = session.get(url, params=args, headers=headers, **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"], ctype)
    return out.json()


def obis_write_disk(url, path, ctype, cache=True, **kwargs):
    """Write API response to disk."""
    cache_instance = get_default_cache(enabled=cache)
    session = cache_instance.get_session()

    out = session.get(url, stream=True, **kwargs)
    out.raise_for_status()
    with open(path, "wb") as f:
        for chunk in out.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return path


def stopifnot(x, ctype):
    """Check if content type matches expected type."""
    if x != ctype:
        raise NoResultException("content-type did not equal " + str(ctype))


def stop(x):
    """Raise ValueError with message."""
    raise ValueError(x)


def handle_arrstr(x):
    """Converts array arguments into comma-separated strings if applicable."""
    if x.__class__.__name__ == "NoneType":
        pass
    else:
        if x.__class__.__name__ == "str":
            return x
        else:
            return ",".join(x)


def handle_arrint(x):
    """Converts array arguments into comma-separated integers if applicable."""
    if x.__class__.__name__ == "NoneType":
        pass
    else:
        if x.__class__.__name__ == "int":
            return x
        else:
            x = list(map(str, x))
            return ",".join(x)
