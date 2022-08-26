import requests
from urllib.parse import urlencode
from ..obisutils import handle_arrstr, obis_baseurl, obis_GET


class OBISQueryResult:
    def __init__(self):
        """
        OBISQueryResult Object for Checklist module
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
        **kwargs
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

            from pyobis import checklist as ch
            ch.list(scientificname = 'Mola mola')

            # taxonid of 3013
            ch.list(taxonid = 3013)
        """
        url = obis_baseurl + "checklist"
        scientificname = handle_arrstr(scientificname)
        out = obis_GET(
            url,
            {
                "taxonid": taxonid,
                "nodeid": nodeid,
                "scientificname": scientificname,
                "startdate": startdate,
                "enddate": enddate,
                "startdepth": startdepth,
                "enddepth": enddepth,
                "geometry": geometry,
                "flags": flags,
            },
            "application/json; charset=utf-8",
            **kwargs
        )
        return out


    def redlist(
        scientificname=None,
        taxonid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        flags=None,
        **kwargs
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

        from pyobis import checklist as ch
        ch.redlist(scientificname='Abra Alba')"""
        url = obis_baseurl + "checklist/redlist"
        scientificname = handle_arrstr(scientificname)
        out = obis_GET(
            url,
            {
                "taxonid": taxonid,
                "nodeid": nodeid,
                "scientificname": scientificname,
                "startdate": startdate,
                "enddate": enddate,
                "startdepth": startdepth,
                "enddepth": enddepth,
                "geometry": geometry,
                "flags": flags,
            },
            "application/json; charset=utf-8",
            **kwargs
        )
        return out


    def newest(
        scientificname=None,
        taxonid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        flags=None,
        **kwargs
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

        from pyobis import checklist as ch
        ch.newest(scientificname='Abra Alba')
        """
        url = obis_baseurl + "checklist/newest"
        scientificname = handle_arrstr(scientificname)
        out = obis_GET(
            url,
            {
                "taxonid": taxonid,
                "nodeid": nodeid,
                "scientificname": scientificname,
                "startdate": startdate,
                "enddate": enddate,
                "startdepth": startdepth,
                "enddepth": enddepth,
                "geometry": geometry,
                "flags": flags,
            },
            "application/json; charset=utf-8",
            **kwargs
        )
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
        return self.url + "?" + urlencode({k:v for k, v in self.args.items() if not v == None})
    
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
        if not self.args["taxonid"] and self.args["scientificname"]:
            self.args["taxonid"] = self.lookup_taxon(self.args["scientificname"])[0]["id"]

        return "https://mapper.obis.org/" + "?" + urlencode({k:v for k, v in self.args.items() if not v == None})
    
    def lookup_taxon(self, scientificname):
        """
        Lookup for taxon metadata with scientificname
        
        :param scientificname: [String] Scientific Name

        :return: A dictionary of taxon metadata for the best matches to the input
        Usage::

            from pyobis.checklist import OBISQueryresult as OQR
            query = OQR()
            lookup_data = query.lookup_taxon(scientificname="Mola mola")
            print(lookup_data)
        """
        res = requests.get(f"https://api.obis.org/v3/taxon/complete/{scientificname}")
        return res.json()
