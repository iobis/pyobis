"""
/nodes/ API endpoints as documented on https://api.obis.org/.
"""
from urllib.parse import urlencode

from ..obisutils import obis_baseurl, obis_GET


class OBISQueryResult:
    def __init__(self):
        """
        An OBISQueryResult object for fetching occurrence records.
        """

    def search(self, id=None, **kwargs):
        """
        Get OBIS nodes records

        :param id: [String] Node UUID.

        :return: A dictionary

        Usage::

            from pyobis import nodes
            nodes.search(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
        """
        self.url = obis_baseurl + "node/" + id
        self.mapper = True
        self.args = {}
        self.nodeid = id  # necessary to get mapper url
        out = obis_GET(self.url, self.args, "application/json; charset=utf-8", **kwargs)

        return out

    def activities(self, id=None, **kwargs):
        """
        Get OBIS nodes activities

        :param id: [String] Node UUID.

        :return: A dictionary

        Usage::

            from pyobis import nodes
            nodes.activities(id="4bf79a01-65a9-4db6-b37b-18434f26ddfc")
        """
        self.url = obis_baseurl + "node/" + id + "/activities"
        self.args = {}
        self.mapper = False
        out = obis_GET(self.url, self.args, "application/json; charset=utf-8", **kwargs)
        return out

    def get_search_url(self):
        """
        Get the corresponding API URL for the query.

        :return: OBIS API URL for the corresponding query

        Usage::

            from pyobis.checklist import OBISQueryresult as OQR
            query = OQR()
            data = query.list(scientificname="Mola mola")
            api_url = query.get_search_url()
            print(api_url)
        """
        return (
            self.url
            + "?"
            + urlencode({k: v for k, v in self.args.items() if v is not None})
        )

    def get_mapper_url(self):
        """
        Get the corresponding API URL for the query.

        :return: OBIS Mapper URL for the corresponding query

        Usage::

            from pyobis.checklist import OBISQueryresult as OQR
            query = OQR()
            data = query.list(scientificname="Mola mola")
            api_url = query.get_mapper_url()
            print(api_url)
        """
        if self.mapper:
            return "https://mapper.obis.org/?nodeid=" + self.nodeid

        return "An OBIS mapper URL doesnot exist for this query"
