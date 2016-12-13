from ..obisutils import *

def group(limit=100, offset=0, **kwargs):
    '''
    Get OBIS groups

    Groups are taxonomic groups

    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import groups
        groups.group()
        groups.group(limit = 3)
        groups.group(limit = 3, offset = 1)
    '''
    url = obis_baseurl + 'group'
    out = obis_GET(url, {'limit': limit, 'offset': offset},
        'application/json;charset=UTF-8', **kwargs)
    return out
