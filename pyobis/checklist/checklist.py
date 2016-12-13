from ..obisutils import *

def list(scientificname=None, aphiaid=None, obisid=None, resourceid=None,
    eezid=None, startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, limit=500, offset=0, **kwargs):
    '''
    Make an OBIS checklist

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq
    :param obisid: [Fixnum] An OBIS id. This is listed as the `id` or `valid_id` in `taxa`/`taxon` results
    :param aphiaid: [Fixnum] An Aphia id. This is listed as the `worms_id` in `taxa`/`taxon` results
    :param resourceid: [Fixnum] An resource id
    :param eezid: [Fixnum] An eez id
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import checklist as ch
        ch.list(scientificname = 'Mola mola')

        # 2005 and Cetacea
        ch.list(year = 2005, scientificname = 'Cetacea')

        # resourceid of 3013
        ch.list(resourceid = 3013)

        # eezid + scientificname
        ch.list(eezid = 59, scientificname = 'Mollusca', limit = 100)

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        ch.list(resourceid = 3013, offset=0, limit=10)
        ch.list(resourceid = 3013, offset=10, limit=10)

        # Get checklist for a particular eventDate
        ch.list(aphiaid=res['worms_id'], year="2013")
    '''
    url = obis_baseurl + 'checklist'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'resourceid': resourceid, 'eezid': eezid, 'scientificname': scientificname,
        'startdate': startdate, 'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'limit': limit, 'offset': offset},
        'application/json;charset=UTF-8', **kwargs)
    return out
