"""
/dataset/ API endpoints as documented on https://api.obis.org/.
"""

from ..obisutils import OBISQueryResult, handle_arrstr, obis_baseurl, obis_GET


class DatasetQuery(OBISQueryResult):
    def __init__(self):
        """
        A DatasetQuery object for fetching dataset records.
        """

    def search(
        self,
        scientificname=None,
        taxonid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        flags=None,
        limit=500,
        offset=0,
        **kwargs
    ):
        """
        Find dataset records.

        :param taxonid: [Fixnum] A obis Taxon AphiaID.
        :param scientificname: [String, Array] One or more scientific names from
            the OBIS backbone. All included and synonym taxa are
            included in the search.
        :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted
            as AD 98. Supports range queries,
            smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
        :param geometry: [String] Well Known Text (WKT). A WKT shape written as
            either POINT, LINESTRING, LINEARRING
            or POLYGON.
            Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would
            be queried as http://bit.ly/1BzNwDq. Geometry, formatted as WKT or
            GeoHash.
        :param nodeid: [Fixnum] Node UUID.
        :param startdate: [Fixnum] Start date
        :param enddate: [Boolean] End date
        :param startdepth: [Fixnum] Start depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param enddepth: [Fixnum] End depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param flags: [String, Array] Comma separated list of quality flags that
            need to be set
        :param offset: [Fixnum] Start at record. Default: 0

        :return: A dictionary

        Usage::

            from pyobis.dataset import DatasetQuery
            dataset = DatasetQuery()
            dataset.search(scientificname = 'Mola mola')

            # Many names
            dataset.search(
                scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria']
            )

            # Use paging parameters (limit and start) to page.
            # Note the different results for the two queries below.
            dataset.search(scientificname = 'Mola mola')
            dataset.search(scientificname = 'Mola mola')

            # Search on a bounding box
            ## in well known text format
            dataset.search(
                geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))'
            )
            from pyobis.taxa import TaxaQuery
            from pyobis.dataset import DatasetQuery
            taxa = TaxaQuery()
            dataset = DatasetQuery()

            res = taxa.search(scientificname='Mola mola')['results'][0]
            dataset.search(
                taxonid=res['id'],
                geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
                limit=20
            )
            dataset.search(
                aphiaid=res['worms_id'],
                geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
                limit=20
            )

            # Get resources for a particular eventDate
            dataset.search(taxonid=res['worms_id'])
        """
        OBISQueryResult.url = obis_baseurl + "dataset"
        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.args = {
            "taxonid": taxonid,
            "nodeid": nodeid,
            "scientificname": scientificname,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "offset": offset,
            "size": limit,
        }
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        self.mapper = False
        return out

    def get(self, id, **kwargs):
        """
        Get dataset by ID

        :param id: [Fixnum] An OBIS dataset identifier.

        :return: A dictionary

        Usage::

            from pyobis.dataset import DatasetQuery
            dataset = DatasetQuery()
            dataset.get('ec9df3b9-3b2b-4d83-881b-27bcbcd57b95')
        """
        OBISQueryResult.url = obis_baseurl + "dataset/" + str(id)
        OBISQueryResult.args = {}
        self.mapper = True
        self.datasetid = str(id)  # necessary to get mapper url
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

            from pyobis.dataset import DatasetQuery
            dataset = DatasetQuery()
            data = dataset.get('ec9df3b9-3b2b-4d83-881b-27bcbcd57b95')
            api_url = dataset.get_mapper_url()
            print(api_url)
        """
        if self.mapper:
            return "https://mapper.obis.org/?datasetid=" + self.datasetid

        return "An OBIS mapper URL doesnot exist for this query"
