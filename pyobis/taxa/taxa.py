from ..obisutils import *

def search(scientificname=None, aphiaid=None, obisid=None, resourceid=None,
    startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, fields=None, limit=500, offset=0, **kwargs):
    '''
    Search OBIS taxa

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone.  All included and synonym taxa
       are included in the search.
    :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq}.
    :param obisid: [Fixnum] An OBIS id. This is listed as the `id` or `valid_id` in `taxa`/`taxon` results
    :param aphiaid: [Fixnum] An Aphia id. This is listed as the `worms_id` in `taxa`/`taxon` results
    :param resourceid: [Fixnum] An resource id
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Booean] End depth
    :param fields: [Array] Array of field names
    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import taxa
        taxa.search(scientificname = 'Mola mola')

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        taxa.search(scientificname = 'Mola mola', offset=0, limit=10)
        taxa.search(scientificname = 'Mola mola', offset=10, limit=10)

        # Search on a bounding box
        ## in well known text format
        taxa.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        from pyobis import taxa
        key = taxa.search(query='Mola mola')[0]['key']
        taxa.search(aphiaid=key, geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)

        # Get taxon for a particular eventDate
        taxa.search(aphiaid=key, year="2013", limit=20)
    '''
    url = obis_baseurl + 'taxa'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'resourceid': resourceid, 'scientificname': scientificname,
        'startdate': startdate, 'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'fields': fields, 'limit': limit, 'offset': offset},
        'application/json;charset=UTF-8', **kwargs)
    return out

def taxon(id, **kwargs):
    '''
    Get taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier

    :return: A dictionary

    Usage::

        from pyobis import taxa
        taxa.taxon(545439)
        taxa.taxon(402913)
        taxa.taxon(406296)
        taxa.taxon(415282)
    '''
    url = obis_baseurl + 'taxon/' + str(id)
    out = obis_GET(url, {}, 'application/json;charset=UTF-8', **kwargs)
    return out

def taxon_search(scientificname=None, aphiaid=None, obisid=None, **kwargs):
    '''
    Get taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier

    :return: A dictionary

    Usage::

        from pyobis import taxa
        taxa.taxon_search(scientificname = 'Mola mola')
        taxa.taxon_search(scientificname = 'Mola')
        taxa.taxon_search(aphiaid = 127405)
        taxa.taxon_search(obisid = 472375)
    '''
    url = obis_baseurl + 'taxon'
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'scientificname': scientificname}, 'application/json;charset=UTF-8', **kwargs)
    return out

def common(id, **kwargs):
    '''
    Get common names for a taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier. Required

    :return: A dictionary

    Usage::

        from pyobis import taxa
        # have common names
        taxa.common(402913)
        taxa.common(406296)
        # no common names
        taxa.common(415282)
    '''
    url = obis_baseurl + 'taxon/' + str(id) + '/common'
    out = obis_GET(url, {}, 'application/json;charset=UTF-8', **kwargs)
    return out
