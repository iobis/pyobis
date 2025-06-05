"""
/taxon/ API endpoints as documented on https://api.obis.org/.
"""

import pandas as pd

from ..obisutils import build_api_url, handle_arrstr, obis_baseurl, obis_GET


def search(scientificname=None, cache=True, **kwargs):
    """
    Get taxon records.

    :param scientificname: [String,Array] One or more scientific names from the
        OBIS backbone. All included and synonym taxa are included in the search
    :param cache: [bool, optional] Whether to use caching. Defaults to True.
    :return: A dictionary

    Usage::

        from pyobis import taxa

        # With caching enabled (default)
        query = taxa.search(scientificname='Mola mola')
        query.execute()

        # With caching disabled
        query = taxa.search(scientificname='Mola mola', cache=False)
        query.execute()

        # Get the data
        query.data # return the fetched data
        query.api_url # get the OBIS API URL for the built query
        query.mapper_url # get the OBIS Mapper URL (if it exists)
    """

    scientificname = handle_arrstr(scientificname)
    url = obis_baseurl + "taxon/" + scientificname
    args = {"scientificname": scientificname}
    # return a taxa response class
    return TaxaResponse(url, args, cache=cache)


def taxon(id, cache=True, **kwargs):
    """
    Get taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier
    :param cache: [bool, optional] Whether to use caching. Defaults to True.
    :return: A TaxaResponse object

    Usage::

        from pyobis import taxa

        # With caching enabled (default)
        query1 = taxa.taxon(545439)
        query1.execute()

        # With caching disabled
        query1 = taxa.taxon(545439, cache=False)
        query1.execute()
    """
    url = obis_baseurl + "taxon/" + str(id)
    args = {}
    # return a TaxaResponse Object
    return TaxaResponse(url, {**args, **kwargs}, cache=cache)


def annotations(scientificname, cache=True, **kwargs):
    """
    Get scientific name annotations by the WoRMS team.

    :param scientificname: [String] Scientific name. Leave empty to include all taxa.
    :param cache: [bool, optional] Whether to use caching. Defaults to True.
    :return: A TaxaResponse Object

    Usage::

        from pyobis import taxa

        # With caching enabled (default)
        query1 = taxa.annotations(scientificname="Abra")
        query1.execute()

        # With caching disabled
        query1 = taxa.annotations(scientificname="Abra", cache=False)
        query1.execute()
    """
    url = obis_baseurl + "taxon/annotations"
    scientificname = handle_arrstr(scientificname)
    args = {"scientificname": scientificname}
    # return a TaxaResponse Object
    return TaxaResponse(url, {**args, **kwargs}, cache=cache)


class TaxaResponse:
    """
    An OBIS Taxa Response Class
    """

    def __init__(self, url, args, cache=True):
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
        self.__cache = cache

    def execute(self, **kwargs):
        """
        Execute or fetch the data based on the query
        """
        out = obis_GET(
            self.__url,
            self.__args,
            "application/json; charset=utf-8",
            cache=self.__cache,
            **kwargs,
        )
        self.data = out
        return self.data

    def to_pandas(self):
        """
        Convert the results into a pandas DataFrame
        """
        return pd.DataFrame(self.data["results"])
