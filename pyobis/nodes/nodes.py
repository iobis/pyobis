from ..obisutils import *

def node(limit=100, offset=0, **kwargs):
    '''
    Get OBIS nodes

    :param limit: [Fixnum] Number of results to return. Default: 1000
    :param offset: [Fixnum] Start at record. Default: 0

    :return: A dictionary

    Usage::

        from pyobis import nodes
        nodes.node()
        nodes.node(limit = 3)
        nodes.node(limit = 3, offset = 1)
    '''
    url = obis_baseurl + 'node'
    out = obis_GET(url, {'limit': limit, 'offset': offset},
        'application/json;charset=UTF-8', **kwargs)
    return out
