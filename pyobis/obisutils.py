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


class OBISQueryResult:
    """
    Return OBIS API URL
    """

    def get_search_url(self):
        """
        Get the corresponding API URL for the query.

        :return: OBIS API URL for the corresponding query

        Usage::

            # supports usage for any query from any module
            from pyobis.taxa import TaxaQuery
            query = TaxaQuery
            query.search(scientificname="Mola mola")
            query.get_search_url()

        """
        return (
            self.url
            + "?"
            + urlencode({k: v for k, v in self.args.items() if v is not None})
        )


def obis_GET(url, args, ctype, **kwargs):
    """Handles technical details of sending GET request to the API"""
    out = requests.get(url, params=args, **kwargs)
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
