from ..obisutils import *

def search(scientificname=None, **kwargs):
    '''
    Get taxon records.
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and synonym taxa
       are included in the search.

    :return: A dictionary

    Usage::

        from pyobis import taxa
        taxa.search(scientificname = 'Mola mola')
        taxa.search(scientificname=['Mola mola','Abra alba'])
    '''
     
    scientificname = handle_arrstr(scientificname)
    url = obis_baseurl + 'taxon/' + scientificname
    
    out = obis_GET(url,{'scientificname': scientificname},'application/json; charset=utf-8', **kwargs)
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
    out = obis_GET(url, {}, 'application/json; charset=utf-8', **kwargs)
    return out

def annotations(scientificname=None, **kwargs):
    '''
    Get scientific name annotations by the WoRMS team.
    :param scientificname: [String] Scientific name. Leave empty to include all taxa.
    :return: A dictionary

    Usage::
        from pyobis import taxa
        taxa.annotations('Abra')
    '''
    url = obis_baseurl + 'taxon/annotations'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'scientificname':scientificname}, 'application/json; charset=utf-8', **kwargs)
    return out
    
def taxon_search(scientificname=None, aphiaid=None, obisid=None, **kwargs):
    '''
    This function has become obsolete.

    :param id: [Fixnum] An OBIS taxon identifier

    :return: A dictionary

    Usage::

        from pyobis import taxa
        taxa.taxon_search(scientificname = 'Mola mola')
        taxa.taxon_search(scientificname = 'Mola')
        taxa.taxon_search(aphiaid = 127405)
        taxa.taxon_search(obisid = 472375)
    '''
    url = obis_baseurl +  'taxon/' + handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'scientificname': scientificname}, 'application/json; charset=utf-8', **kwargs)
    return out
    
def common(id, **kwargs):
    '''
    This function has become obsolete.
    
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
    out = obis_GET(url, {}, 'application/json; charset=utf-8', **kwargs)
    return out