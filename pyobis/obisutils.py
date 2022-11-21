"""
Utility functions for internal use across various modules.
"""
from urllib.parse import urlencode

import requests

obis_baseurl = "https://api.obis.org/v3/"


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


def obis_GET(url, args, ctype, **kwargs):
    """
    Handles technical details of sending GET request to the API
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "api.obis.org",
        "Connection": "keep-alive",
    }
    out = requests.get(url, params=args, headers=headers, **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"], ctype)
    return out.json()


def obis_write_disk(url, path, ctype, **kwargs):
    out = requests.get(url, stream=True, **kwargs)
    out.raise_for_status()
    with open(path, "wb") as f:
        for chunk in out.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return path


def stopifnot(x, ctype):
    if x != ctype:
        raise NoResultException("content-type did not equal " + str(ctype))


def stop(x):
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
