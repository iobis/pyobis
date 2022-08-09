import sys
from tkinter.messagebox import NO

import pandas as pd

from ..obisutils import *


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

    :param taxonid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param year: Removed in v3 API. [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq
    :param nodeid: [String] Node UUID
    :param taxonid: Prev. aphiaid [Fixnum] An Aphia id. This is listed as the `worms_id` in `taxa`/`taxon` results
    :param datasetid: Prev. resourceid [Fixnum] A resource id
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param flags: Prev. qc [String] Quality control flags
    :param fields: [String] Comma seperated list of field names
    :param size: [Fixnum] Number of results to return. Default: All records
    :param offset: [Fixnum] Start at record. Default: 0
    :param mof: [Boolean] Include MeasurementOrFact records, true/false. Default: 0
    :param hasextensions: [String] Extensions that need to be present (e.g. MeasurementOrFact, DNADerivedData).
    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.search(scientificname = 'Mola mola')

        # Many names
        occ.search(scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria'])

        # Use paging parameters (limit and start) to page. Note the different results
        # for the two queries below.
        occ.search(scientificname = 'Mola mola', offset=0, size=10)
        occ.search(scientificname = 'Mola mola', offset=10, size=10)

        # Search on a bounding box
        ## in well known text format
        occ.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
        from pyobis import taxa
        res = taxa.search(scientificname='Mola mola')['results'][0]
        occ.search(obisid=res['id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', size=20)
        occ.search(aphiaid=res['worms_id'], geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', size=20)

        # Get mof response as list of pandas dataframes
        occ.search(scientificname="Abra",mof=True,hasextensions="MeasurementOrFact")
    """
    url = obis_baseurl + "occurrence"
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
        "size": 0,
        "hasextensions": hasextensions,
    }
    out = obis_GET(url, args, "application/json; charset=utf-8", **kwargs)
    size = (
        out["total"] if not size else size
    )  # if the user has set some size or else we fetch all the records
    for i in range(5000, size + 1, 5000):
        if (
            args["size"] != 0
        ):  # this condition is to make sure that we set the `after` parameter when fetching subsequent records only, and first batch gets fetched correctly without this `after` parameter
            args["after"] = res["results"][4999]["id"]
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
        res = obis_GET(url, args, "application/json; charset=utf-8", **kwargs)
        out["results"] += res["results"]
    args["size"] = (
        size % 5000
    )  # we have already fetched records as a set of 5000 records each time, now we need to get remaining records from the total
    print(
        "{}[{}{}] {}/{}".format("Fetching: ", "█" * 100, "." * 0, size, size),
        end="\r",
        file=sys.stdout,
        flush=True,
    )
    res = obis_GET(url, args, "application/json; charset=utf-8", **kwargs)
    out["results"] += res["results"]
    print(f"\nFetched {size} records.")

    if mof and out["total"] > 0:
        mofNormalized = pd.json_normalize(out["results"], "mof", ["id"])
        merged = pd.merge(
            pd.DataFrame(out["results"]),
            mofNormalized,
            on="id",
            how="inner",
        )
        return merged
    return out


def get(id, **kwargs):
    """
    Get an OBIS occurrence

    :param id: [Fixnum] An obis occurrence identifier. It is returned in the 'id' field with occurrences.search().

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.get(id = '00008e33-6faa-4d98-a00b-91a6ed1ed3ca')
    """
    url = obis_baseurl + "occurrence/" + str(id)
    out = obis_GET(url, {}, "application/json; charset=utf-8", **kwargs)
    return out


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
    :param scientificname: [string] Scientific name. Leave empty to include all taxa.
    :param taxonid: [string] Taxon AphiaID.
    :param datasetid: [string] Dataset UUID.
    :param nodeid: [string] Node UUID.
    :param startdate: [string] Start date formatted as YYYY-MM-DD.
    :param enddate: [string] End date formatted as YYYY-MM-DD.
    :param startdepth: [integer] Start depth, in meters.
    :param enddepth: [integer] End depth, in meters.
    :param geometry: [string] Geometry, formatted as WKT or GeoHash.
    :param redlist: [boolean] Red List species only, True/False.
    :param hab: [boolean] HAB species only, true/false.
    :param wrims: [boolean] WRiMS species only, True/False.
    :param event: [string] Include pure event records (include) or get pure event records exclusively (true).
    :param flags: [string] Comma separated list of quality flags which need to be set.
    :param exclude: [string] Comma separated list of quality flags to be excluded.

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.grid(100, True) // returns in GeoJSON format
        occ.grid(1000, False)   // returns in KML format
    """
    url = obis_baseurl + "occurrence/grid/" + str(precision)
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
        out = requests.get(url + "/kml", params=args, **kwargs)
        out.raise_for_status()
        stopifnot(out.headers["content-type"], "text/xml; charset=utf-8")
        return out.content
    out = obis_GET(url, args, "application/json; charset=utf-8", **kwargs)
    return out


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

    :param scientificname: [string] Scientific name. Leave empty to include all taxa.
    :param taxonid: [string] Taxon AphiaID.
    :param datasetid: [string] Dataset UUID.
    :param nodeid: [string] Node UUID.
    :param startdate: [string] Start date formatted as YYYY-MM-DD.
    :param enddate: [string] End date formatted as YYYY-MM-DD.
    :param startdepth: [integer] Start depth, in meters.
    :param enddepth: [integer] End depth, in meters.
    :param geometry: [string] Geometry, formatted as WKT or GeoHash.
    :param redlist: [boolean] Red List species only, True/False.
    :param hab: [boolean] HAB species only, true/false.
    :param wrims: [boolean] WRiMS species only, True/False.
    :param event: [string] Include pure event records (include) or get pure event records exclusively (true).
    :param flags: [string] Comma separated list of quality flags which need to be set.
    :param exclude: [string] Comma separated list of quality flags to be excluded.

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.getpoints(scientificname = 'Mola mola')

        ## Many names
        occ.getpoints(scientificname = ['Mola mola','Abra alba'])
    """
    url = obis_baseurl + "occurrence/points"
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(
        url,
        {
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
        },
        "application/json; charset=utf-8",
        **kwargs,
    )
    return out


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
    Fetch point occurrences for a location (with Geohash precision 8 or variable Geohash precision) as GeoJSON.

    :param x: [float] latitudes of a location
    :param y: [float] laongitude of a location
    :param z: [float] zoom level, if present then variable Geohash precision, if absent then precision 8
    :param scientificname: [string] Scientific name. Leave empty to include all taxa.
    :param taxonid: [string] Taxon AphiaID.
    :param datasetid: [string] Dataset UUID.
    :param nodeid: [string] Node UUID.
    :param startdate: [string] Start date formatted as YYYY-MM-DD.
    :param enddate: [string] End date formatted as YYYY-MM-DD.
    :param startdepth: [integer] Start depth, in meters.
    :param enddepth: [integer] End depth, in meters.
    :param geometry: [string] Geometry, formatted as WKT or GeoHash.
    :param redlist: [boolean] Red List species only, True/False.
    :param hab: [boolean] HAB species only, true/false.
    :param wrims: [boolean] WRiMS species only, True/False.
    :param event: [string] Include pure event records (include) or get pure event records exclusively (true).
    :param flags: [string] Comma separated list of quality flags which need to be set.
    :param exclude: [string] Comma separated list of quality flags to be excluded.

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.point(x=1.77,y=54.22,scientificname = 'Mola mola')

    """
    z = str(z) if z else ""
    url = obis_baseurl + f"occurrence/point/{str(x)}/{str(y)}/{z}"
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(
        url,
        {
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
        },
        "application/json; charset=utf-8",
        **kwargs,
    )
    return out


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
    Fetch point occurrences for a tile (aggregated using variable Geohash precision based on zoom level) as GeoJSON or MVT.

    :param x: [float] latitudes of a location
    :param y: [float] laongitude of a location
    :param z: [float] zoom level
    :param scientificname: [string] Scientific name. Leave empty to include all taxa.
    :param taxonid: [string] Taxon AphiaID.
    :param datasetid: [string] Dataset UUID.
    :param nodeid: [string] Node UUID.
    :param startdate: [string] Start date formatted as YYYY-MM-DD.
    :param enddate: [string] End date formatted as YYYY-MM-DD.
    :param startdepth: [integer] Start depth, in meters.
    :param enddepth: [integer] End depth, in meters.
    :param geometry: [string] Geometry, formatted as WKT or GeoHash.
    :param redlist: [boolean] Red List species only, True/False.
    :param hab: [boolean] HAB species only, true/false.
    :param wrims: [boolean] WRiMS species only, True/False.
    :param event: [string] Include pure event records (include) or get pure event records exclusively (true).
    :param flags: [string] Comma separated list of quality flags which need to be set.
    :param exclude: [string] Comma separated list of quality flags to be excluded.

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.tile(x=1.77,y=52.26,z=0.5,mvt=0, scientificname = 'Mola mola')
        occ.tile(x=1.77,y=52.26,z=0.5,mvt=1, scientificname = 'Mola mola')
    """
    url = obis_baseurl + f"occurrence/tile/{str(x)}/{str(y)}/{str(z)}"
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
    scientificname = handle_arrstr(scientificname)

    if mvt:
        out = requests.get(url + ".mvt", params=args, **kwargs)
        out.raise_for_status()
        # stopifnot(out.headers['content-type'], "text/xml; charset=utf-8")
        return out.content

    out = obis_GET(url, args, "application/json; charset=utf-8", **kwargs)
    return out


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

    :param scientificname: [string] Scientific name. Leave empty to include all taxa.
    :param taxonid: [string] Taxon AphiaID.
    :param datasetid: [string] Dataset UUID.
    :param nodeid: [string] Node UUID.
    :param startdate: [string] Start date formatted as YYYY-MM-DD.
    :param enddate: [string] End date formatted as YYYY-MM-DD.
    :param startdepth: [integer] Start depth, in meters.
    :param enddepth: [integer] End depth, in meters.
    :param geometry: [string] Geometry, formatted as WKT or GeoHash.
    :param redlist: [boolean] Red List species only, True/False.
    :param hab: [boolean] HAB species only, true/false.
    :param wrims: [boolean] WRiMS species only, True/False.
    :param event: [string] Include pure event records (include) or get pure event records exclusively (true).
    :param flags: [string] Comma separated list of quality flags which need to be set.
    :param exclude: [string] Comma separated list of quality flags to be excluded.

    :return: A dictionary

    Usage::

        from pyobis import occurrences as occ
        occ.centroid(scientificname = 'Mola mola')
    """
    url = obis_baseurl + "occurrence/centroid"
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(
        url,
        {
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
        },
        "application/json; charset=utf-8",
        **kwargs,
    )
    return out
