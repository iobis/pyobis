from ..obisutils import *

def search(scientificname=None, aphiaid=None, obisid=None, resourceid=None,
    startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, fields=None, limit=500, offset=0, **kwargs):
    '''
    Search OBIS taxa

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificname: A scientific name from the obis backbone. All included and synonym taxa are included in the search.
    :param year: The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: Searches for occurren
       Text (WKT) format. A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq}.
    :param obisid: (integer) An OBIS id
    :param aphiaid: (integer) An Aphia id
    :param resourceid: (integer) An resource id
    :param startdate: (integer) Start date
    :param enddate: (logical) End date
    :param startdepth: (integer) Start depth
    :param enddepth: (logical) End depth
    :param fields: [Array] Array of field names
    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary, of results

    Usage::

        from pyobis import taxon
        taxon.search(scientificname = 'Mola mola')

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        taxon.search(scientificname = 'Mola mola', offset=0, limit=10)
        taxon.search(scientificname = 'Mola mola', offset=10, limit=10)

        # Search on a bounding box
        ## in well known text format
        taxon.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        from pyobis import taxa
        key = taxa.search(query='Mola mola')[0]['key']
        taxon.search(aphiaid=key, geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)

        # Get taxon for a particular eventDate
        taxon.search(aphiaid=key, year="2013", limit=20)

        # Query based on quality control flags
        taxon.search(aphiaid=1, issue='DEPTH_UNLIKELY')
        taxon.search(aphiaid=1, issue=['DEPTH_UNLIKELY','COORDINATE_ROUNDED'])
        # Show all records in the Arizona State Lichen Collection that cant be matched to the obis
        # backbone properly:
        taxon.search(datasetKey='84c0e1a0-f762-11e1-a439-00145eb45e9a', issue=['TAXON_MATCH_NONE','TAXON_MATCH_HIGHERRANK'])
    '''
    url = obis_baseurl + 'taxon'
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'resourceid': resourceid, 'scientificname': scientificname,
        'startdate': startdate, 'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'fields': fields, 'limit': limit, 'offset': offset}, **kwargs)
    return out

def taxon(id=None, **kwargs):
    '''
    Get taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier
    :return: A dictionary, of results

    Usage::

        from pyobis import taxon
        taxon.taxon(545439)
        taxon.taxon(402913)
        taxon.taxon(406296)
        taxon.taxon(415282)
    '''
    url = obis_baseurl + 'taxon/' + str(id)
    out = obis_GET(url, {}, **kwargs)
    return out
