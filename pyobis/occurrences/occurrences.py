"""
/occurrences/ API endpoints as documented on https://api.obis.org/.
"""

import json
import sys
from urllib.parse import urlencode

import pandas as pd
import requests

from ..obisutils import (
    build_api_url,
    handle_arrint,
    handle_arrstr,
    obis_baseurl,
    obis_GET,
)


class OccResponse:
    """
    An OBIS Occurrence response class
    """

    def __init__(self, url, args, isSearch, hasMapper, isKML):
        """ "
        Initialise the object parameters
        """
        self.data = None
        self.api_url = build_api_url(url, args)
        self.mapper_url = None
        if hasMapper:
            if not args["taxonid"] and args["scientificname"]:
                args["taxonid"] = lookup_taxon(args["scientificname"])[0]["id"]

            self.mapper_url = (
                "https://mapper.obis.org/"
                + "?"
                + urlencode(
                    {k: v for k, v in args.items() if v is not None},
                )
            )

        # private members
        self.__args = args
        self.__url = url
        self.__isSearch = isSearch
        self.__isKML = isKML

    def execute(self, **kwargs):
        """
        Execute or fetch the data based on the query
        """
        if not self.__isSearch and not self.__isKML:
            out = obis_GET(
                self.__url, self.__args, "application/json; charset=utf-8", **kwargs
            )

        elif self.__isKML:
            print("hello")
            out = requests.get(self.__url, params=self.__args, **kwargs)
            out.raise_for_status()
            out = out.content

        elif self.__isSearch:
            # setting default parameters from arguments list
            mof = self.__args["mof"]
            size = self.__args["size"]

            self.__args["size"] = 1
            out = obis_GET(
                self.__url, self.__args, "application/json; charset=utf-8", **kwargs
            )
            size = (
                out["total"] if not size else size
            )  # if the user has set some size or else we fetch all the records

            outdf = pd.DataFrame(columns=pd.DataFrame(out["results"]).columns)

            for i in range(5000, size + 1, 5000):
                self.__args["size"] = 5000
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
                    self.__url, self.__args, "application/json; charset=utf-8", **kwargs
                )
                outdf = pd.concat(
                    [
                        outdf.infer_objects(),
                        pd.DataFrame(res["results"]).infer_objects(),
                    ],
                    ignore_index=True,
                )
                # make sure that we set the `after` parameter when fetching subsequent records
                self.__args["after"] = outdf["id"].iloc[-1]

            self.__args["size"] = size % 5000
            # we have already fetched records as a set of 5000 records each time,
            # now we need to get remaining records from the total
            print(
                "{}[{}{}] {}/{}".format("Fetching: ", "█" * 100, "." * 0, size, size),
                end="\r",
                file=sys.stdout,
                flush=True,
            )
            res = obis_GET(
                self.__url, self.__args, "application/json; charset=utf-8", **kwargs
            )
            outdf = pd.concat(
                [outdf.infer_objects(), pd.DataFrame(res["results"]).infer_objects()],
                ignore_index=True,
            )
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
                self.data = merged
                return self.data
            self.data = outdf
            return self.data
        self.data = out
        return self.data

    def to_pandas(self):
        """
        Convert the results into a pandas DataFrame
        """
        return pd.DataFrame(self.data["results"])


def get(id, **kwargs):
    """
    Get an OBIS occurrence

    :param id: [Fixnum] An obis occurrence identifier.
        It is returned in the 'id' field with occurrences.search().

    :return: A dictionary

    Usage::

        from pyobis import occurrences
        q1 = occurrences.get(id = '00003cf7-f2fc-4c53-98a6-7d846e70f5d1')
        q1.execute()
        q1.data # get the data
        q1.api_url # get the API url

    """
    url = obis_baseurl + "occurrence/" + str(id)
    args = {}

    return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=False)


def search(
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

        from pyobis import occurrences
        occurrences.search(scientificname = 'Mola mola').execute()

        # Many names
        occurrences.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria']).execute()

        # Use paging parameters (limit and start) to page.
        # Note the different results for the two queries below.
        occ.search(scientificname = 'Mola mola', offset=0, size=10)
        occ.search(scientificname = 'Mola mola', offset=10, size=10)

        # Search on a bounding box
        ## in well known text format
        occurrences.search(
            geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
            size=20
        ).execute()

        from pyobis import taxa

        res = taxa.search(scientificname='Mola mola').execute()['results'][0]
        occurrences.search(
            obisid=res['id'],
            geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
            size=20
        ).execute()
        occurrences.search(
            aphiaid=res['worms_id'],
            geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
            size=20
        ).execute()

        # Get mof response as a pandas dataframe
        occurrences.search(
            scientificname="Abra", mof=True, hasextensions="MeasurementOrFact", size=100
            ).execute()
    """
    url = obis_baseurl + "occurrence"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
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
        "size": size,
        "hasextensions": hasextensions,
    }
    return OccResponse(url, args, isSearch=True, hasMapper=True, isKML=False)


def grid(
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

        from pyobis import occurrences

        occurrences.grid(100, True) // returns in GeoJSON format
        ococcurrences.grid(1000, False)   // returns in KML format
    """
    url = obis_baseurl + "occurrence/grid/" + str(precision)
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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
    if not geojson:
        url += "/kml"
        return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=True)

    return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=False)


def getpoints(
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

        from pyobis import occurrences
        occurrences.getpoints(scientificname = 'Mola mola')

        ## Many names
        occurrences.getpoints(scientificname = ['Mola mola','Abra alba'])
    """
    url = obis_baseurl + "occurrence/points"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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

    return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=False)


def point(
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

        from pyobis import occurrences
        occurrences.point(x=1.77,y=54.22,scientificname = 'Mola mola')

    """
    z = str(z) if z else ""
    url = obis_baseurl + f"occurrence/point/{str(x)}/{str(y)}/{z}"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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

    return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=False)


def tile(
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

        from pyobis import occurrences
        occurrences.tile(x=1.77,y=52.26,z=0.5,mvt=0, scientificname = 'Mola mola')
        occurrences.tile(x=1.77,y=52.26,z=0.5,mvt=1, scientificname = 'Mola mola')
    """
    url = obis_baseurl + f"occurrence/tile/{str(x)}/{str(y)}/{str(z)}"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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
    if mvt:
        url += ".mvt"
        return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=True)

    return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=False)


def centroid(
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

        from pyobis import occurrences
        occurrences.centroid(scientificname = 'Mola mola')
    """
    url = obis_baseurl + "occurrence/centroid"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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

    return OccResponse(url, args, isSearch=False, hasMapper=False, isKML=False)


def lookup_taxon(scientificname):
    """
    Lookup for taxon metadata with scientificname

    :param scientificname: [String] Scientific Name

    :return: A dictionary of taxon metadata for the best matches to the input

    Usage::

        from pyobis import occurrences
        lookup_data = occurrences.lookup_taxon(scientificname="Mola mola")
        print(lookup_data)
    """
    res = requests.get(f"https://api.obis.org/v3/taxon/complete/{scientificname}")
    return res.json()
