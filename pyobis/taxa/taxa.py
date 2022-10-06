"""
/taxon/ API endpoints as documented on https://api.obis.org/.
"""
from ..obisutils import build_api_url, handle_arrstr, obis_baseurl, obis_GET
import pandas as pd

def search(scientificname=None, **kwargs):
    """
    Get taxon records.

    :param scientificname: [String,Array] One or more scientific names from the
        OBIS backbone. All included and synonym taxa are included in the search

    :return: A dictionary

    Usage::

        from pyobis.taxa import TaxaQuery
        taxa = TaxaQuery()
        taxa.search(scientificname = 'Mola mola')
        taxa.search(scientificname=['Mola mola','Abra alba'])
    """

    scientificname = handle_arrstr(scientificname)
    url = obis_baseurl + "taxon/" + scientificname
    args = {"scientificname": scientificname}
    # return a taxa response class
    
    return TaxaResponse(url, args)

def taxon(self, id, **kwargs):
    """
    Get taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier

    :return: A TaxaResponse object

    Usage::

        from pyobis import taxa
        query1 = taxa.taxon(545439)
        query1.execute()
        # executes the query previously built from OBIS
        query1.data
        # returns the data
        query1.api_url
        # returns the OBIS API URL
        query1.mapper_url
        # returns the OBIS Mapper URL for easy visualization
        
        taxa.taxon(402913).execute().data
        q2 = taxa.taxon(406296)
        q3 = taxa.taxon(415282)
    """
    url = obis_baseurl + "taxon/" + str(id)
    args = {}
    # return a TaxaResponse Object
    return TaxaResponse(url, args)

def annotations(self, scientificname, **kwargs):
    """
    Get scientific name annotations by the WoRMS team.

    :param scientificname: [String] Scientific name. Leave empty to include all taxa.
    :return: A TaxaResponse Object

    Usage::

        from pyobis import taxa
        query1 = taxa.annotations(scientificname="Abra")
        query1.execute()
        # executes the query previously built from OBIS
        query1.data
        # returns the data
        query1.api_url
        # returns the OBIS API URL
        query1.mapper_url
        # returns the OBIS Mapper URL for easy visualization      
        
    """
    url = obis_baseurl + "taxon/annotations"
    scientificname = handle_arrstr(scientificname)
    args = {"scientificname": scientificname}
    # return a TaxaResponse Object
    return TaxaResponse(url, args)

class TaxaResponse():
    """
    Taxa Response Class
    """
    def __init__(self, url, args):
        # public members
        self.data = None
        self.api_url = build_api_url(url, args)
        self.mapper_url = None
        
        # protected members
        self.__args = args
        self.__url = url
    
    def execute(self, **kwargs):
        out = obis_GET(
            self.__url,
            self.__args,
            "application/json; charset=utf-8",
            **kwargs
            )
        self.data = out
    
    def to_pandas(self):
        return pd.DataFrame(self.data["results"])
