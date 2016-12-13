from ..obisutils import *

def search(scientificname=None, aphiaid=None, obisid=None, resourceid=None,
    startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, qc=None, fields=None, limit=500, offset=0, **kwargs):
    '''
    Search OBIS occurrences

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
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param qc: [String] Quality control flags
    :param fields: [Array] Array of field names
    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.search(scientificname = 'Mola mola')

        # Many names
        occ.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        occ.search(scientificname = 'Mola mola', offset=0, limit=10)
        occ.search(scientificname = 'Mola mola', offset=10, limit=10)

        # Search on a bounding box
        ## in well known text format
        occ.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        from pyobis import taxa
        res = taxa.search(scientificname='Mola mola')['results'][0]
        occ.search(obisid=res['id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        occ.search(aphiaid=res['worms_id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)

        # Get occurrences for a particular eventDate
        occ.search(aphiaid=res['worms_id'], year="2013", limit=20)
    '''
    url = obis_baseurl + 'occurrence'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'resourceid': resourceid, 'scientificname': scientificname,
        'startdate': startdate, 'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'fields': fields, 'qc': qc, 'limit': limit, 'offset': offset},
        'application/json;charset=UTF-8', **kwargs)
    return out


def get(id, **kwargs):
    '''
    Get an OBIS occurrence

    :param id: [Fixnum] An obis occurrence identifier

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.get(id = 14333)
        occ.get(id = 135355)

        # many at once
        [ occ.get(id = x) for x in [14333, 135355, 276413] ]
    '''
    url = obis_baseurl + 'occurrence/' + str(id)
    out = obis_GET(url, {}, 'application/json;charset=UTF-8', **kwargs)
    return out
