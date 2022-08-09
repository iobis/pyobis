from ..obisutils import *


def list(
    scientificname=None,
    taxonid=None,
    nodeid=None,
    startdate=None,
    enddate=None,
    startdepth=None,
    enddepth=None,
    geometry=None,
    flags=None,
    **kwargs
):
    """
    Generate an OBIS checklist

    :param taxonid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq
    :param nodeid: [Fixnum] Node UUID.
    :param startdate: [String] Start date YYYY-MM-DD
    :param enddate: [String] End date YYYY-MM-DD
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param flags: [String] Comma separated list of quality flags which need to be set

    :return: A dictionary

    Usage::

        from pyobis import checklist as ch
        ch.list(scientificname = 'Mola mola')

        # taxonid of 3013
        ch.list(taxonid = 3013)
    """
    url = obis_baseurl + "checklist"
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(
        url,
        {
            "taxonid": taxonid,
            "nodeid": nodeid,
            "scientificname": scientificname,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "flags": flags,
        },
        "application/json; charset=utf-8",
        **kwargs
    )
    return out


def redlist(
    scientificname=None,
    taxonid=None,
    nodeid=None,
    startdate=None,
    enddate=None,
    startdepth=None,
    enddepth=None,
    geometry=None,
    flags=None,
    **kwargs
):
    """
    Generate a checklist of IUCN Red List species.

    :param scientificname: [String] Scientific name. Leave empty to include all taxa.
    :param taxonid: [String] Taxon AphiaID.
    :param nodeid: [String] Node UUID.
    :param startdate: [String] Start date formatted as YYYY-MM-DD.
    :param enddate: [String] End date formatted as YYYY-MM-DD.
    :param startdepth: [Integer] Start depth, in meters.
    :param enddepth: [Integer] End depth, in meters.
    :param geometry: [String] Geometry, formatted as WKT or GeoHash.
    :param flags: [String] Comma separated list of quality flags which need to be set.

    :return: A dictionary

    Usage::

       from pyobis import checklist as ch
       ch.redlist(scientificname='Abra Alba')"""
    url = obis_baseurl + "checklist/redlist"
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(
        url,
        {
            "taxonid": taxonid,
            "nodeid": nodeid,
            "scientificname": scientificname,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "flags": flags,
        },
        "application/json; charset=utf-8",
        **kwargs
    )
    return out


def newest(
    scientificname=None,
    taxonid=None,
    nodeid=None,
    startdate=None,
    enddate=None,
    startdepth=None,
    enddepth=None,
    geometry=None,
    flags=None,
    **kwargs
):
    """
    Generate a checklist of most recently added species.

    :param scientificname: [String] Scientific name. Leave empty to include all taxa.
    :param taxonid: [String] Taxon AphiaID.
    :param nodeid: [String] Node UUID.
    :param startdate: [String] Start date formatted as YYYY-MM-DD.
    :param enddate: [String] End date formatted as YYYY-MM-DD.
    :param startdepth: [Integer] Start depth, in meters.
    :param enddepth: [Integer] End depth, in meters.
    :param geometry: [String] Geometry, formatted as WKT or GeoHash.
    :param flags: [String] Comma separated list of quality flags which need to be set.

    :return: A dictionary

    Usage::

       from pyobis import checklist as ch
       ch.newest(scientificname='Abra Alba')
    """
    url = obis_baseurl + "checklist/newest"
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(
        url,
        {
            "taxonid": taxonid,
            "nodeid": nodeid,
            "scientificname": scientificname,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "flags": flags,
        },
        "application/json; charset=utf-8",
        **kwargs
    )
    return out
