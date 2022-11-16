"""
/nodes/ API endpoints as documented on https://api.obis.org/.
"""

import pandas as pd

from ..obisutils import build_api_url, obis_baseurl, obis_GET


def search(id=None, **kwargs):
    """
    Get OBIS nodes records

    :param id: [String] Node UUID.

    :return: A NodesQuery Object

    Usage::

        from pyobis import nodes
        data = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc").execute()
    """
    url = obis_baseurl + "node/" + id
    mapper = True
    args = {}

    # return NodesQuery Object
    return NodesResponse(url, args, mapper)


def activities(id=None, **kwargs):
    """
    Get OBIS nodes activities

    :param id: [String] Node UUID.

    :return: A NodesQuery object

    Usage::

        from pyobis import nodes

        # build a query
        query = nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
        query.execute() # execute the query to fetch the data
        query.data # get fetched data
        query.api_url # check the corresponding OBIS API URL for the query
        query.mapper_url # check the corresponding OBIS Mapper URL for the query (if it exists)
    """
    url = obis_baseurl + "node/" + id + "/activities"
    args = {}
    mapper = False

    # return a NodesQuery object
    return NodesResponse(url, args, mapper)


class NodesResponse:
    """
    An OBIS Nodes Response Class
    """

    def __init__(self, url, args, mapper):
        """
        Initialize NodesResponse Object
        """
        # public members
        self.data = None
        self.api_url = build_api_url(url, args)
        self.mapper_url = None
        if mapper:
            # get the node id from already built url
            self.mapper_url = f"https://mapper.obis.org/?nodeid={url.split('/')[-1]}"

        # private members
        self.__args = args
        self.__url = url

    def execute(self, **kwargs):
        """
        Fetch data for Nodes Query
        """
        out = obis_GET(
            self.__url, self.__args, "application/json; charset=utf-8", **kwargs
        )
        self.data = out
        return self.data

    def to_pandas(self):
        """
        Convert fetched data to a pandas DataFrame
        """
        if "contacts" in self.data["results"][0].keys():
            return pd.merge(
                pd.DataFrame(self.data["results"]),
                pd.json_normalize(self.data["results"], "contacts", "id"),
                on="id",
                how="inner",
            ).drop("contacts", axis=1)

        return pd.merge(
            pd.DataFrame(self.data["results"]),
            pd.json_normalize(self.data["results"], "contributions", "id"),
            on="id",
            how="inner",
        ).drop("contributions", axis=1)
