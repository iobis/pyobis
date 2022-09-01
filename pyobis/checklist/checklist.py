"""
/checklist/ API endpoints as documented on https://api.obis.org/.
"""

from ..obisutils import OBISQueryResult, handle_arrstr, obis_baseurl, obis_GET


class ChecklistQuery(OBISQueryResult):
    def __init__(self):
        """
        ChecklistQuery Object for Checklist module
        """
        pass

    def list(
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
        **kwargs,
    ):
        """
        Generate an OBIS checklist

        :param taxonid: [Fixnum] A obis occurrence identifier
        :param scientificname: [String,Array] One or more scientific names from
            the OBIS backbone. All included and synonym taxa are included in
            the search.
        :param geometry: [String] Well Known Text (WKT). A WKT shape written as
            either POINT, LINESTRING, LINEARRING
            or POLYGON.
            Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would
            be queried as http://bit.ly/1BzNwDq
        :param nodeid: [Fixnum] Node UUID.
        :param startdate: [String] Start date YYYY-MM-DD
        :param enddate: [String] End date YYYY-MM-DD
        :param startdepth: [Fixnum] Start depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param enddepth: [Fixnum] End depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param flags: [String] Comma separated list of quality flags which need
            to be set

        :return: A dictionary

        Usage::

            from pyobis.checklist import ChecklistQuery
            ch = ChecklistQuery()
            ch.list(scientificname = 'Mola mola')

            # taxonid of 3013
            ch.list(taxonid = 3013)
        """
        OBISQueryResult.url = obis_baseurl + "checklist"
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
            "flags": flags,
        }
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def redlist(
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
        **kwargs,
    ):
        """
        Generate a checklist of IUCN Red List species.

        :param scientificname: [String] Scientific name. Leave empty to include
            all taxa.
        :param taxonid: [String] Taxon AphiaID.
        :param nodeid: [String] Node UUID.
        :param startdate: [String] Start date formatted as YYYY-MM-DD.
        :param enddate: [String] End date formatted as YYYY-MM-DD.
        :param startdepth: [Fixnum] Start depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param enddepth: [Fixnum] End depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param geometry: [String] Geometry, formatted as WKT or GeoHash.
        :param flags: [String] Comma separated list of quality flags which need
            to be set.

        :return: A dictionary

        Usage::

            from pyobis.checklist import ChecklistQuery
            ch = ChecklistQuery()
            ch.redlist(scientificname='Abra Alba')
        """
        OBISQueryResult.url = obis_baseurl + "checklist/redlist"
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
            "flags": flags,
        }
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def newest(
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
        **kwargs,
    ):
        """
        Generate a checklist of most recently added species.

        :param scientificname: [String] Scientific name. Leave empty to include
            all taxa.
        :param taxonid: [String] Taxon AphiaID.
        :param nodeid: [String] Node UUID.
        :param startdate: [String] Start date formatted as YYYY-MM-DD.
        :param enddate: [String] End date formatted as YYYY-MM-DD.
        :param startdepth: [Fixnum] Start depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param enddepth: [Fixnum] End depth, in meters. Depth below sea level are treated as
            positive numbers.
        :param geometry: [String] Geometry, formatted as WKT or GeoHash.
        :param flags: [String] Comma separated list of quality flags which need to
            be set.

        :return: A dictionary

        Usage::

            from pyobis.checklist import ChecklistQuery
            ch = ChecklistQuery()
            ch.newest(scientificname='Abra Alba')
        """
        OBISQueryResult.url = obis_baseurl + "checklist/newest"
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
            "flags": flags,
        }
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out
