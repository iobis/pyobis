from ..obisutils import *

def search(scientificName=None, aphiaid=None, obisid=None, startdate=None,
    enddate=None, geometry=None, year=None, qc=None, limit=500,
    offset=0, **kwargs):
    '''
    Search OBIS occurrences

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificName: A scientific name from the obis backbone. All included and synonym taxa are included in the search.
    :param year: The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: Searches for occurrences inside a polygon described in Well Known
       Text (WKT) format. A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq}.
    :param obisid: (integer) An OBIS id
    :param aphiaid: (integer) An Aphia id
    :param startdate: (integer) Start date
    :param enddate: (logical) End date
    :param qc: (character) One or more of many possible issues with each occurrence record
    :param limit: [Fixnum] Number of results to return.
    :param offset: [Fixnum] Start at record X

    :return: A dictionary, of results

    Usage::

        from pyobis import occurrences
        occurrences.search(scientificName = 'Mola mola')

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        occurrences.search(scientificName = 'Mola mola', offset=0, limit=10)
        occurrences.search(scientificName = 'Mola mola', offset=10, limit=10)

        # Search on a bounding box
        ## in well known text format
        occurrences.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        from pyobis import taxa
        key = taxa.search(query='Mola mola')[0]['key']
        occurrences.search(aphiaid=key, geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)

        # Get occurrences for a particular eventDate
        occurrences.search(aphiaid=key, year="2013", limit=20)

        # Query based on quality control flags
        occurrences.search(aphiaid=1, issue='DEPTH_UNLIKELY')
        occurrences.search(aphiaid=1, issue=['DEPTH_UNLIKELY','COORDINATE_ROUNDED'])
        # Show all records in the Arizona State Lichen Collection that cant be matched to the obis
        # backbone properly:
        occurrences.search(datasetKey='84c0e1a0-f762-11e1-a439-00145eb45e9a', issue=['TAXON_MATCH_NONE','TAXON_MATCH_HIGHERRANK'])
    '''
    url = obis_baseurl + 'occurrence'
    out = obis_GET(url, {'aphiaid': aphiaid, 'scientificName': scientificName,
        'obisid': obisid, 'geometry': geometry, 'year': year, 'qc': qc,
        'limit': limit, 'offset': offset}, **kwargs)
    return out
