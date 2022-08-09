from ..obisutils import *


def search(id=None, **kwargs):
    """
    Get OBIS nodes records

    :param id: [String] Node UUID.

    :return: A dictionary

    Usage::

        from pyobis import nodes
        nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    """
    url = obis_baseurl + "node/" + id
    out = obis_GET(url, {}, "application/json; charset=utf-8", **kwargs)
    return out


def activities(id=None, **kwargs):
    """
    Get OBIS nodes activities

    :param id: [String] Node UUID.

    :return: A dictionary

    Usage::

        from pyobis import nodes
        nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
    """
    url = obis_baseurl + "node/" + id + "/activities"
    out = obis_GET(url, {}, "application/json; charset=utf-8", **kwargs)
    return out
