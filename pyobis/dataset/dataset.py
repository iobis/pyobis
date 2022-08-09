from ..obisutils import *


def search(
    scientificname=None,
    taxonid=None,
    nodeid=None,
    startdate=None,
    enddate=None,
    startdepth=None,
    enddepth=None,
    geometry=None,
    flags=None,
    limit=500,
    offset=0,
    **kwargs
):
    """
    Find dataset records.

    :param taxonid: [Fixnum] A obis Taxon AphiaID.
    :param scientificname: [String, Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq. Geometry, formatted as WKT or GeoHash.
    :param nodeid: [Fixnum] Node UUID.
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param flags: [String, Array] Comma separated list of quality flags which need to be set
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import dataset
        dataset.search(scientificname = 'Mola mola')

        # Many names
        dataset.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        dataset.search(scientificname = 'Mola mola')
        dataset.search(scientificname = 'Mola mola')

        # Search on a bounding box
        ## in well known text format
        dataset.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))')
        from pyobis import taxa
        res = taxa.search(scientificname='Mola mola')['results'][0]
        dataset.search(taxonid=res['id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        dataset.search(aphiaid=res['worms_id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)

        # Get resources for a particular eventDate
        dataset.search(taxonid=res['worms_id'])
    """
    url = obis_baseurl + "dataset"
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
            "offset": offset,
        },
        "application/json; charset=utf-8",
        **kwargs
    )
    return out


def get(id, **kwargs):
    """
    Get dataset by ID

    :param id: [Fixnum] An OBIS dataset identifier.

    :return: A dictionary

    Usage::

        from pyobis import dataset
        dataset.get('ec9df3b9-3b2b-4d83-881b-27bcbcd57b95')
    """
    url = obis_baseurl + "dataset/" + str(id)
    out = obis_GET(url, {}, "application/json; charset=utf-8", **kwargs)
    return out
