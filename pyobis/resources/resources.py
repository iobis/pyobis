from ..obisutils import *

def search(scientificname=None, aphiaid=None, obisid=None,
    startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, limit=500, offset=0, **kwargs):
    '''
    Search OBIS resources

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq
    :param obisid: [Fixnum] An OBIS id. This is listed as the `id` or `valid_id` in `taxa`/`taxon` results
    :param aphiaid: [Fixnum] An Aphia id. This is listed as the `worms_id` in `taxa`/`taxon` results
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import resources
        resources.search(scientificname = 'Mola mola')

        # Many names
        resources.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        resources.search(scientificname = 'Mola mola', offset=0, limit=3)
        resources.search(scientificname = 'Mola mola', offset=10, limit=2)

        # Search on a bounding box
        ## in well known text format
        resources.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        from pyobis import taxa
        res = taxa.search(scientificname='Mola mola')['results'][0]
        resources.search(obisid=res['id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        resources.search(aphiaid=res['worms_id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)

        # Get resources for a particular eventDate
        resources.search(aphiaid=res['worms_id'], year="2013", limit=20)
    '''
    url = obis_baseurl + 'resource'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'scientificname': scientificname, 'startdate': startdate,
        'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'limit': limit, 'offset': offset}, 'application/json;charset=UTF-8', **kwargs)
    return out

def resource(id, **kwargs):
    '''
    Get resource by ID

    :param id: [Fixnum] An OBIS resource identifier

    :return: A dictionary

    Usage::

        from pyobis import resources
        resources.resource(103)
        resources.resource(2126)
    '''
    url = obis_baseurl + 'resource/' + str(id)
    out = obis_GET(url, {}, 'application/json;charset=UTF-8', **kwargs)
    return out

def citation(scientificname=None, aphiaid=None, obisid=None,
    startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, limit=500, offset=0, **kwargs):
    '''
    List dataset citations

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq
    :param obisid: [Fixnum] An OBIS id. This is listed as the `id` or `valid_id` in `taxa`/`taxon` results
    :param aphiaid: [Fixnum] An Aphia id. This is listed as the `worms_id` in `taxa`/`taxon` results
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import resources
        resources.citation(scientificname = 'Mola mola')

        # Many names
        resources.citation(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        resources.citation(scientificname = 'Mola mola', offset=0, limit=10)
        resources.citation(scientificname = 'Mola mola', offset=10, limit=10)
    '''
    url = obis_baseurl + 'citation'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'scientificname': scientificname, 'startdate': startdate,
        'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'limit': limit, 'offset': offset},
        'application/json;charset=UTF-8', **kwargs)
    return out
