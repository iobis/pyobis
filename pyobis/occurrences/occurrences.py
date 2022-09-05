"""
/occurrences/ API endpoints as documented on https://api.obis.org/.
"""

import json
import sys
from urllib.parse import urlencode

import pandas as pd
import requests

from ..obisutils import (
    OBISQueryResult,
    handle_arrstr,
    obis_baseurl,
    obis_GET,
    stopifnot,
)


class OccQuery(OBISQueryResult):
    def __init__(self):
        """
        An OccQuery object for fetching occurrence records.
        """

    def search(
        self,
        scientificname=None,
        taxonid=None,
        nodeid=None,
        datasetid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        year=None,
        flags=None,
        fields=None,
        size=None,
        offset=0,
        mof=False,
        hasextensions=None,
        **kwargs,
    ):
        """
        Search OBIS occurrences

        :param taxonid: [Fixnum] An OBIS occurrence identifier
        :param scientificname: [String,Array] One or more scientific names from the
            OBIS backbone. All included and
            synonym taxa are included in the search.
        :param year: Removed in v3 API. [Fixnum] The 4 digit year. A year of 98
            will be interpreted as AD 98. Supports range queries,
            smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
        :param geometry: [String] Well Known Text (WKT). A WKT shape written
            as either POINT, LINESTRING, LINEARRING
            or POLYGON.
            Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would
            be queried as http://bit.ly/1BzNwDq
        :param nodeid: [String] Node UUID
        :param taxonid: Prev. aphiaid [Fixnum] An Aphia id. This is listed as
            the `worms_id` in `taxa`/`taxon` results
        :param datasetid: Prev. resourceid [Fixnum] A resource id
        :param startdate: [Fixnum] Start date, formatted as YYYY-MM-DD
        :param enddate: [Boolean] End date, formatted as YYYY-MM-DD
        :param startdepth: [Fixnum] Start depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param enddepth: [Boolean] End depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param flags: Prev. qc [String] Quality control flags
        :param fields: [String] Comma seperated list of field names
        :param size: [Fixnum] Number of results to return. Default: All records
        :param offset: [Fixnum] Start at record. Default: 0
        :param mof: [Boolean] Include MeasurementOrFact records, true/false.
            Default: 0
        :param hasextensions: [String] Extensions that need to be present
            (e.g. MeasurementOrFact, DNADerivedData).
        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.search(scientificname = 'Mola mola')

            # Many names
            occ.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])

            # Use paging parameters (limit and start) to page.
            # Note the different results for the two queries below.
            occ.search(scientificname = 'Mola mola', offset=0, size=10)
            occ.search(scientificname = 'Mola mola', offset=10, size=10)

            # Search on a bounding box
            ## in well known text format
            occ.search(
                geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
                size=20
            )
            from pyobis.taxa import TaxaQuery
            taxa = TaxaQuery()
            res = taxa.search(scientificname='Mola mola')['results'][0]
            occ.search(
                obisid=res['id'],
                geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
                size=20
            )
            occ.search(
                aphiaid=res['worms_id'],
                geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
                size=20
            )

            # Get mof response as a pandas dataframe
            occ.search(scientificname="Abra", mof=True, hasextensions="MeasurementOrFact", size=100)
        """
        OBISQueryResult.url = obis_baseurl + "occurrence"
        scientificname = handle_arrstr(scientificname)
        args = {
            "taxonid": taxonid,
            "nodeid": nodeid,
            "datasetid": datasetid,
            "scientificname": scientificname,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "year": year,
            "fields": fields,
            "flags": flags,
            "offset": offset,
            "mof": mof,
            "size": 1,
            "hasextensions": hasextensions,
        }
        OBISQueryResult.args = args
        self.mapper = True
        out = obis_GET(
            OBISQueryResult.url, args, "application/json; charset=utf-8", **kwargs
        )
        size = (
            out["total"] if not size else size
        )  # if the user has set some size or else we fetch all the records

        outdf = pd.DataFrame(columns=pd.DataFrame(out["results"]).columns)

        for i in range(5000, size + 1, 5000):
            args["size"] = 5000
            print(
                "{}[{}{}] {}/{}".format(
                    "Fetching: ",
                    "█" * int((i - 1) * 100 / size),
                    "." * (100 - int((i + 1) * 100 / size)),
                    i,
                    size,
                ),
                end="\r",
                file=sys.stdout,
                flush=True,
            )
            res = obis_GET(
                OBISQueryResult.url, args, "application/json; charset=utf-8", **kwargs
            )
            outdf = pd.concat([outdf, pd.DataFrame(res["results"])], ignore_index=True)
            # make sure that we set the `after` parameter when fetching subsequent records
            args["after"] = outdf["id"].iloc[-1]

        args["size"] = size % 5000
        # we have already fetched records as a set of 5000 records each time,
        # now we need to get remaining records from the total
        print(
            "{}[{}{}] {}/{}".format("Fetching: ", "█" * 100, "." * 0, size, size),
            end="\r",
            file=sys.stdout,
            flush=True,
        )
        res = obis_GET(
            OBISQueryResult.url, args, "application/json; charset=utf-8", **kwargs
        )
        outdf = pd.concat([outdf, pd.DataFrame(res["results"])], ignore_index=True)
        print(f"\nFetched {size} records.")

        if mof and out["total"] > 0:
            mofNormalized = pd.json_normalize(
                json.loads(outdf.to_json(orient="records")),
                "mof",
                ["id"],
            )
            merged = pd.merge(
                outdf,
                mofNormalized,
                on="id",
                how="inner",
            )
            return merged
        return outdf

    def get(self, id, **kwargs):
        """
        Get an OBIS occurrence

        :param id: [Fixnum] An obis occurrence identifier.
            It is returned in the 'id' field with occurrences.search().

        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.get(id = '00008e33-6faa-4d98-a00b-91a6ed1ed3ca')
        """
        OBISQueryResult.url = obis_baseurl + "occurrence/" + str(id)
        OBISQueryResult.args = {}
        self.mapper = False
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def grid(
        self,
        precision,
        geojson=True,
        scientificname=None,
        taxonid=None,
        datasetid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        redlist=None,
        hab=None,
        wrims=None,
        event=None,
        flags=None,
        exclude=None,
        **kwargs,
    ):
        """
        Fetch gridded occurrences as GeoJSON or KML.

        :param precision: [integer] Geohash precision.
        :param scientificname: [string] Scientific name.
            Leave empty to include all taxa.
        :param taxonid: [string] Taxon AphiaID.
        :param datasetid: [string] Dataset UUID.
        :param nodeid: [string] Node UUID.
        :param startdate: [string] Start date formatted as YYYY-MM-DD.
        :param enddate: [string] End date formatted as YYYY-MM-DD.
        :param startdepth: [integer] Start depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param enddepth: [integer] End depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param geometry: [string] Geometry, formatted as WKT or GeoHash.
        :param redlist: [boolean] Red List species only, True/False.
        :param hab: [boolean] HAB species only, true/false.
        :param wrims: [boolean] WRiMS species only, True/False.
        :param event: [string] Include pure event records (include) or get pure
            event records exclusively (true).
        :param flags: [string] Comma separated list of required quality flags.
        :param exclude: [string] Comma separated list of quality flags
            to be excluded.

        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.grid(100, True) // returns in GeoJSON format
            occ.grid(1000, False)   // returns in KML format
        """
        OBISQueryResult.url = obis_baseurl + "occurrence/grid/" + str(precision)
        OBISQueryResult.args = {
            "scientificname": scientificname,
            "taxonid": taxonid,
            "datasetid": datasetid,
            "nodeid": nodeid,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "redlist": redlist,
            "hab": hab,
            "wrims": wrims,
            "event": event,
            "flags": flags,
            "exclude": exclude,
        }
        self.mapper = False
        if not geojson:
            OBISQueryResult.url += "/kml"
            out = requests.get(
                OBISQueryResult.url, params=OBISQueryResult.args, **kwargs
            )
            out.raise_for_status()
            stopifnot(out.headers["content-type"], "text/xml; charset=utf-8")
            return out.content
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def getpoints(
        self,
        scientificname=None,
        taxonid=None,
        datasetid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        redlist=None,
        hab=None,
        wrims=None,
        event=None,
        flags=None,
        exclude=None,
        **kwargs,
    ):
        """
        Fetch point occurrences as GeoJSON (aggregated to Geohash precision 8).

        :param scientificname: [string] Scientific name. Leave empty to include all
            taxa.
        :param taxonid: [string] Taxon AphiaID.
        :param datasetid: [string] Dataset UUID.
        :param nodeid: [string] Node UUID.
        :param startdate: [string] Start date formatted as YYYY-MM-DD.
        :param enddate: [string] End date formatted as YYYY-MM-DD.
        :param startdepth: [integer] Start depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param enddepth: [integer] End depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param geometry: [string] Geometry, formatted as WKT or GeoHash.
        :param redlist: [boolean] Red List species only, True/False.
        :param hab: [boolean] HAB species only, true/false.
        :param wrims: [boolean] WRiMS species only, True/False.
        :param event: [string] Include pure event records (include) or get pure0
            event records exclusively (true).
        :param flags: [string] Comma separated list of quality flags which need to
            be set.
        :param exclude: [string] Comma separated list of quality flags to be
            excluded.

        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.getpoints(scientificname = 'Mola mola')

            ## Many names
            occ.getpoints(scientificname = ['Mola mola','Abra alba'])
        """
        OBISQueryResult.url = obis_baseurl + "occurrence/points"
        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.args = {
            "scientificname": scientificname,
            "taxonid": taxonid,
            "datasetid": datasetid,
            "nodeid": nodeid,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "redlist": redlist,
            "hab": hab,
            "wrims": wrims,
            "event": event,
            "flags": flags,
            "exclude": exclude,
        }
        self.mapper = False
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def point(
        self,
        x,
        y,
        z=None,
        scientificname=None,
        taxonid=None,
        datasetid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        redlist=None,
        hab=None,
        wrims=None,
        event=None,
        flags=None,
        exclude=None,
        **kwargs,
    ):
        """
        Fetch point occurrences for a location (with Geohash precision 8 or
        variable Geohash precision) as GeoJSON.

        :param x: [float] latitudes of a location
        :param y: [float] longitude of a location
        :param z: [float] vertical datum (geodatic datum WGS84)
        :param scientificname: [string] Scientific name. Leave empty to include all
            taxa.
        :param taxonid: [string] Taxon AphiaID.
        :param datasetid: [string] Dataset UUID.
        :param nodeid: [string] Node UUID.
        :param startdate: [string] Start date formatted as YYYY-MM-DD.
        :param enddate: [string] End date formatted as YYYY-MM-DD.
        :param startdepth: [integer] Start depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param enddepth: [integer] End depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param geometry: [string] Geometry, formatted as WKT or GeoHash.
        :param redlist: [boolean] Red List species only, True/False.
        :param hab: [boolean] HAB species only, true/false.
        :param wrims: [boolean] WRiMS species only, True/False.
        :param event: [string] Include pure event records (include) or get pure
            event records exclusively (true).
        :param flags: [string] Comma separated list of quality flags which need
            to be set.
        :param exclude: [string] Comma separated list of quality flags to be
            excluded.

        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.point(x=1.77,y=54.22,scientificname = 'Mola mola')

        """
        z = str(z) if z else ""
        OBISQueryResult.url = obis_baseurl + f"occurrence/point/{str(x)}/{str(y)}/{z}"
        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.args = {
            "scientificname": scientificname,
            "taxonid": taxonid,
            "datasetid": datasetid,
            "nodeid": nodeid,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "redlist": redlist,
            "hab": hab,
            "wrims": wrims,
            "event": event,
            "flags": flags,
            "exclude": exclude,
        }
        self.mapper = False
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def tile(
        self,
        x,
        y,
        z,
        mvt=0,
        scientificname=None,
        taxonid=None,
        datasetid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        redlist=None,
        hab=None,
        wrims=None,
        event=None,
        flags=None,
        exclude=None,
        **kwargs,
    ):
        """
        Fetch point occurrences for a tile (aggregated using variable Geohash
        precision based on zoom level) as GeoJSON or MVT.

        :param x: [float] latitudes of a location
        :param y: [float] longitude of a location
        :param z: [float] vertical datum (geodatic datum WGS84)
        :param scientificname: [string] Scientific name. Leave empty to include
            all taxa.
        :param taxonid: [string] Taxon AphiaID.
        :param datasetid: [string] Dataset UUID.
        :param nodeid: [string] Node UUID.
        :param startdate: [string] Start date formatted as YYYY-MM-DD.
        :param enddate: [string] End date formatted as YYYY-MM-DD.
        :param startdepth: [integer] Start depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param enddepth: [integer] End depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param geometry: [string] Geometry, formatted as WKT or GeoHash.
        :param redlist: [boolean] Red List species only, True/False.
        :param hab: [boolean] HAB species only, true/false.
        :param wrims: [boolean] WRiMS species only, True/False.
        :param event: [string] Include pure event records (include) or get pure
            event records exclusively (true).
        :param flags: [string] Comma separated list of quality flags which need to
            be set.
        :param exclude: [string] Comma separated list of quality flags to be
            excluded.

        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.tile(x=1.77,y=52.26,z=0.5,mvt=0, scientificname = 'Mola mola')
            occ.tile(x=1.77,y=52.26,z=0.5,mvt=1, scientificname = 'Mola mola')
        """
        OBISQueryResult.url = (
            obis_baseurl + f"occurrence/tile/{str(x)}/{str(y)}/{str(z)}"
        )
        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.args = {
            "scientificname": scientificname,
            "taxonid": taxonid,
            "datasetid": datasetid,
            "nodeid": nodeid,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "redlist": redlist,
            "hab": hab,
            "wrims": wrims,
            "event": event,
            "flags": flags,
            "exclude": exclude,
        }
        self.mapper = False
        if mvt:
            OBISQueryResult.url += ".mvt"
            out = requests.get(
                OBISQueryResult.url, params=OBISQueryResult.args, **kwargs
            )
            out.raise_for_status()
            # stopifnot(out.headers['content-type'], "text/xml; charset=utf-8")
            return out.content

        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def centroid(
        self,
        scientificname=None,
        taxonid=None,
        datasetid=None,
        nodeid=None,
        startdate=None,
        enddate=None,
        startdepth=None,
        enddepth=None,
        geometry=None,
        redlist=None,
        hab=None,
        wrims=None,
        event=None,
        flags=None,
        exclude=None,
        **kwargs,
    ):
        """
        Determine the centroid for a selection of occurrence records.

        :param scientificname: [string] Scientific name. Leave empty to include all
            taxa.
        :param taxonid: [string] Taxon AphiaID.
        :param datasetid: [string] Dataset UUID.
        :param nodeid: [string] Node UUID.
        :param startdate: [string] Start date formatted as YYYY-MM-DD.
        :param enddate: [string] End date formatted as YYYY-MM-DD.
        :param startdepth: [integer] Start depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param enddepth: [integer] End depth, in meters. Depth below sea level are treated
            as positive numbers.
        :param geometry: [string] Geometry, formatted as WKT or GeoHash.
        :param redlist: [boolean] Red List species only, True/False.
        :param hab: [boolean] HAB species only, true/false.
        :param wrims: [boolean] WRiMS species only, True/False.
        :param event: [string] Include pure event records (include) or get pure
            event records exclusively (true).
        :param flags: [string] Comma separated list of required quality flags.
        :param exclude: [string] Comma separated list of quality flags to be
            excluded.

        :return: A dictionary

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            occ.centroid(scientificname = 'Mola mola')
        """
        OBISQueryResult.url = obis_baseurl + "occurrence/centroid"
        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.args = {
            "scientificname": scientificname,
            "taxonid": taxonid,
            "datasetid": datasetid,
            "nodeid": nodeid,
            "startdate": startdate,
            "enddate": enddate,
            "startdepth": startdepth,
            "enddepth": enddepth,
            "geometry": geometry,
            "redlist": redlist,
            "hab": hab,
            "wrims": wrims,
            "event": event,
            "flags": flags,
            "exclude": exclude,
        }
        self.mapper = False
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs,
        )
        return out

    def get_mapper_url(self):
        """
        Get the corresponding API URL for the query.

        :return: OBIS Mapper URL for the corresponding query

        Note: For correct output, query for records using multiple (single) Taxon IDs or one
        Scientific Name.

        Usage::

            from pyobis.occurrences import OccQuery
            occ = OccQuery()
            data = occ.search(scientificname="Mola mola", size=20)
            api_url = occ.get_mapper_url()
            print(api_url)
        """
        if self.mapper:
            if (
                not OBISQueryResult.args["taxonid"]
                and OBISQueryResult.args["scientificname"]
            ):
                OBISQueryResult.args["taxonid"] = self.lookup_taxon(
                    OBISQueryResult.args["scientificname"],
                )[0]["id"]

            return (
                "https://mapper.obis.org/"
                + "?"
                + urlencode(
                    {k: v for k, v in OBISQueryResult.args.items() if v is not None},
                )
            )
        return "An OBIS mapper URL doesnot exist for this query"

    def lookup_taxon(self, scientificname):
        """
        Lookup for taxon metadata with scientificname

        :param scientificname: [String] Scientific Name

        :return: A dictionary of taxon metadata for the best matches to the input

        Usage::

            from pyobis.occurrences import OccQuery
            query = OccQuery()
            lookup_data = query.lookup_taxon(scientificname="Mola mola")
            print(lookup_data)
        """
        res = requests.get(f"https://api.obis.org/v3/taxon/complete/{scientificname}")
        return res.json()
