"""
/nodes/ API endpoints as documented on https://api.obis.org/.
"""

from ..obisutils import OBISQueryResult, obis_baseurl, obis_GET


class NodesQuery(OBISQueryResult):
    def __init__(self):
        """
        A NodesQuery object for fetching Nodes records.
        """

    def search(self, id=None, **kwargs):
        """
        Get OBIS nodes records

        :param id: [String] Node UUID.

        :return: A dictionary

        Usage::

            from pyobis.nodes import NodesQuery
            nodes = NodesQuery()
            nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
        """
        OBISQueryResult.url = obis_baseurl + "node/" + id
        self.mapper = True
        OBISQueryResult.args = {}
        self.nodeid = id  # necessary to get mapper url
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs
        )

        return out

    def activities(self, id=None, **kwargs):
        """
        Get OBIS nodes activities

        :param id: [String] Node UUID.

        :return: A dictionary

        Usage::

            from pyobis.nodes import NodesQuery
            nodes = NodesQuery()
            nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
        """
        OBISQueryResult.url = obis_baseurl + "node/" + id + "/activities"
        OBISQueryResult.args = {}
        self.mapper = False
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        return out

    def get_mapper_url(self):
        """
        Get the corresponding API URL for the query.

        :return: OBIS Mapper URL for the corresponding query

        Usage::

            from pyobis.nodes import NodesQuery
            nodes = NodesQuery()
            data = nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
            api_url = nodes.get_mapper_url()
            print(api_url)
        """
        if self.mapper:
            return "https://mapper.obis.org/?nodeid=" + self.nodeid

        return "An OBIS mapper URL doesnot exist for this query"
