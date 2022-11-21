"""
/taxon/ API endpoints as documented on https://api.obis.org/.
"""
import pandas as pd

from ..obisutils import build_api_url, handle_arrstr, obis_baseurl, obis_GET


def search(scientificname=None, **kwargs):
    """
    Get taxon records.

    :param scientificname: [String,Array] One or more scientific names from the
        OBIS backbone. All included and synonym taxa are included in the search

    :return: A dictionary

    Usage::

        from pyobis import taxa

        # build a query
        query = taxa.search(scientificname = 'Mola mola')
        query.execute() # execute the query i.e. fetch the data
        query.data # return the fetched data
        query.api_url # get the OBIS API URL for the built query
        query.mapper_url # get the OBIS Mapper URL (if it exists)

        # or simply get the data in one-easy step
        data = taxa.search(scientificname=['Mola mola','Abra alba']).execute()
    """

    scientificname = handle_arrstr(scientificname)
    url = obis_baseurl + "taxon/" + scientificname
    args = {"scientificname": scientificname}
    # return a taxa response class

    return TaxaResponse(url, args)


def taxon(id, **kwargs):
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

        taxa.taxon(402913).execute()
        q2 = taxa.taxon(406296)
        q3 = taxa.taxon(415282)
    """
    url = obis_baseurl + "taxon/" + str(id)
    args = {}
    # return a TaxaResponse Object
    return TaxaResponse(url, args)


def annotations(scientificname, **kwargs):
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


class TaxaResponse:
    """
    An OBIS Taxa Response Class
    """

    def __init__(self, url, args):
        """
        Initialise the object parameters
        """
        # public members
        self.data = None
        self.api_url = build_api_url(url, args)
        self.mapper_url = None

        # private members
        self.__args = args
        self.__url = url

    def execute(self, **kwargs):
        """
        Execute or fetch the data based on the query
        """
        out = obis_GET(
            self.__url, self.__args, "application/json; charset=utf-8", **kwargs
        )
        self.data = out
        return self.data

    def to_pandas(self):
        """
        Convert the results into a pandas DataFrame
        """
        return pd.DataFrame(self.data["results"])
