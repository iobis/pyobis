"""
/checklist/ API endpoints as documented on https://api.obis.org/.
"""
import sys

import pandas as pd

from ..obisutils import (
    build_api_url,
    handle_arrint,
    handle_arrstr,
    obis_baseurl,
    obis_GET,
)


class ChecklistResponse:
    """
    An OBIS Checklist Response Object
    """

    def __init__(self, url, args, paginate):
        """
        Initialise the object parameters
        """
        self.api_url = build_api_url(url, args)
        self.mapper_url = None
        self.data = None

        # private members
        self.__url = url
        self.__args = args
        self.__paginate = paginate

    def execute(self):
        """
        Execute or fetch the data based on the query
        """
        if self.__paginate:
            out = obis_GET(
                self.__url,
                self.__args,
                "application/json; charset=utf-8",
            )
            self.__args["skip"] += 10
            self.__args["size"] = 5000
            i = 10

            # an error check is necessary, otherwise print statement throws "division by zero" error
            try:
                out["error"]
                return out["error"]
            except KeyError:
                pass

            # fetch first 10 records, and print number of estimated records
            print(f"Estimated records: {out['total']}")
            print(
                "{}[{}{}] {}".format(
                    "Fetching: ",
                    "█" * int(len(out["results"]) * 100 / out["total"]),
                    "." * (100 - int(len(out["results"]) * 100 / out["total"])),
                    len(out["results"]),
                ),
                end="\r",
                file=sys.stdout,
                flush=True,
            )
            # now paginate until the response is null
            while True:
                res = obis_GET(
                    self.__url,
                    self.__args,
                    "application/json; charset=utf-8",
                )
                # when we find that no records are there, we break out of loop
                if len(res["results"]) == 0:
                    break
                out["results"] += res["results"]
                # print the progress bar
                print(
                    "{}[{}{}] {}".format(
                        "Fetching: ",
                        "█" * int(len(out["results"]) * 100 / out["total"]),
                        "." * (100 - int(len(out["results"]) * 100 / out["total"])),
                        len(out["results"]),
                    ),
                    end="\r",
                    file=sys.stdout,
                    flush=True,
                )
                self.__args["skip"] = len(out["results"])
                # continue to fetch next 5000 records
                i += 5000
            # print actual number of fetched records
            print(f"\nFetched {len(out['results'])} records.")
        else:
            out = obis_GET(
                self.__url,
                self.__args,
                "application/json; charset=utf-8",
            )
        self.data = out

    def to_pandas(self):
        """
        Convert the results into a pandas DataFrame
        """
        return pd.DataFrame(self.data["results"])


def list(
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

        from pyobis import checklist
        checklist.list(scientificname = 'Mola mola').execute()

        # taxonid of 3013
        checklist.list(taxonid = 3013).execute()
    """
    url = obis_baseurl + "checklist"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
        "taxonid": taxonid,
        "nodeid": nodeid,
        "scientificname": scientificname,
        "startdate": startdate,
        "enddate": enddate,
        "startdepth": startdepth,
        "enddepth": enddepth,
        "geometry": geometry,
        "flags": flags,
        "skip": 0,
        "size": 10,
    }

    return ChecklistResponse(url, args, paginate=True)


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

        from pyobis import checklist
        checklist.redlist(scientificname='Abra Alba').execute()
    """
    url = obis_baseurl + "checklist/redlist"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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

    return ChecklistResponse(url, args, paginate=False)


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

        from pyobis import checklist
        checklist.newest(scientificname='Abra Alba')
    """
    url = obis_baseurl + "checklist/newest"
    scientificname = handle_arrstr(scientificname)
    taxonid = handle_arrint(taxonid)
    args = {
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

    return ChecklistResponse(url, args, paginate=False)
