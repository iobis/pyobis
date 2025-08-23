"""
/dataset/ API endpoints as documented on https://api.obis.org/.
"""

import pandas as pd

from ..obisutils import build_api_url, handle_arrstr, obis_baseurl, obis_GET


def search(
    scientificname=None,
    taxonid=None,
    nodeid=None,
    startdate=None,
    enddate=None,
    startdepth=None,
    enddepth=None,
    geometry=None,
    flags=None,
    limit=None,
    offset=0,
    cache=True,
    keyword=None,
    **kwargs,
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
        Example of a polygon: ((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1)) would
        be queried as https://api.obis.org/v3/occurrence?geometry=POLYGON%28%2830.1+10.1%2C+10+20%2C+20+40%2C+40+40%2C+30.1+10.1%29%29
        Geometry, formatted as WKT or GeoHash.
    :param nodeid: [Fixnum] Node UUID.
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth, in meters. Depth below sea level are treated as
        positive numbers.
    :param enddepth: [Fixnum] End depth, in meters. Depth below sea level are treated as
        positive numbers.
    :param flags: [String, Array] Comma separated list of quality flags that
        need to be set
    :param keyword: [String] Keyword(s) to search for in dataset metadata.
        When `keyword` is used, no other filter parameters may be specified.
        Uses Elasticsearch `simple_query_string` syntax with support for:
          - `+` (AND), e.g., `coral+reef`
          - quotes `"..."` for exact phrases, e.g., `"coral reef"`
          - `|` (OR), e.g., `coral|kelp`
          - `-` (NOT), e.g., `coral -fish`
          - trailing wildcards `*`, e.g., `star*`
          - grouping with parentheses, e.g., `(coral | kelp) -fish`
        Leading or mid-word wildcards (e.g., `*star` or `*star*`) are not supported.
    :param offset: [Fixnum] Start at record. Default: 0
    :param cache: [bool, optional] Whether to use caching. Defaults to True.

    :return: A DatasetResponse object

    Usage::

        from pyobis import dataset
        query = dataset.search(scientificname = 'Mola mola')
        data = query.execute() # or query.data

        # Many names
        dataset.search(
            scientificname = ['Mola', 'Abra', 'Lanice', 'Pectinaria']
        ).execute()

        # Use paging parameters (limit and start) to page.
        # Note the different results for the two queries below.
        # build the query
        query = dataset.search(scientificname = 'Mola mola')
        query.execute() # fetch the data
        query.data # return the data
        dataset.search(scientificname = 'Mola mola').execute() # or simply one-easy step

        # Search on a bounding box
        ## in well known text format
        dataset.search(
            geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))'
        ).execute()
        from pyobis import taxa
        from pyobis import dataset

        res = taxa.search(scientificname='Mola mola').execute().data['results'][0]
        dataset.search(
            taxonid=res['id'],
            geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
            limit=20
        ).execute()
        dataset.search(
            aphiaid=res['worms_id'],
            geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))',
            limit=20
        ).execute()

        # Get resources for a particular eventDate
        data = dataset.search(taxonid=res['worms_id']).execute()
    """  # noqa: E501
    LOCALS = locals()
    url = obis_baseurl + "dataset"

    # =================================================================================
    # === Keyword-only metadata search path (Elasticsearch simple_query_string via `q`)
    # =================================================================================
    if keyword is not None:
        # === check for other kwargs not compatible with keyword
        allowed_with_keyword = {"limit", "offset", "cache"}
        __validate_keyword_constraints(keyword, allowed_with_keyword, LOCALS, kwargs)
        args = {
            "q": keyword,
            "offset": offset,
            "size": limit,
        }
        mapper = False
        return DatasetResponse(url, {**args, **kwargs}, mapper, cache=cache)
    # =================================================================================
    # === non-keyword-based search
    # =================================================================================
    scientificname = handle_arrstr(scientificname)
    args = {
        "taxonid": taxonid,
        "nodeid": nodeid,
        "scientificname": scientificname,
        "startdate": startdate,
        "enddate": enddate,
        "startdepth": startdepth,
        "enddepth": enddepth,
        "geometry": geometry,
        "offset": offset,
        "flags": flags,
        "size": limit,
    }

    mapper = False
    return DatasetResponse(url, {**args, **kwargs}, mapper, cache=cache)
    # =================================================================================


def get(id, cache=True, **kwargs):
    """
    Get dataset by ID

    :param id: [Fixnum] An OBIS dataset identifier.
    :param cache: [bool, optional] Whether to use caching. Defaults to True.
    :return: A DatasetResponse object

    Usage::

        from pyobis import dataset
        query = dataset.get('ec9df3b9-3b2b-4d83-881b-27bcbcd57b95')
        query.execute() # execute the query
        query.data # returns the data of the query
        query.api_url # returns the OBIS API URL
    """
    url = obis_baseurl + "dataset/" + str(id)
    args = {}
    mapper = True

    # returns a DatasetResponse object
    return DatasetResponse(url, {**args, **kwargs}, mapper, cache=cache)


class DatasetResponse:
    """
    An OBIS Dataset Response Object
    """

    def __init__(self, url, args, mapper, cache=True):
        """
        Initialise the object parameters
        """
        # public members
        self.data = None
        self.api_url = build_api_url(url, args)
        self.mapper_url = None
        if mapper:
            self.mapper_url = f"https://mapper.obis.org/?datasetid={url.split('/')[-1]}"

        # private members
        self.__args = args
        self.__url = url
        self.__cache = cache

    def execute(self, **kwargs):
        """
        Execute or fetch the data based on the query
        """
        out = obis_GET(
            self.__url,
            self.__args,
            "application/json; charset=utf-8",
            cache=self.__cache,
            **kwargs,
        )
        self.data = out
        return self.data

    def to_pandas(self):
        """
        Convert the results into a pandas DataFrame
        """
        return pd.DataFrame(self.data["results"])


def __validate_keyword_constraints(
    keyword,
    allowed_with_keyword,
    all_args,
    extra_kwargs,
):
    """
    Ensure that if `keyword` is provided, no other disallowed parameters are set.

    Parameters
    ----------
    keyword : any
        The value of the `keyword` argument from the caller.
    allowed_with_keyword : set
        Names of parameters that are allowed to be non-None when keyword is given.
    all_args : dict
        Dict of *all* arguments (e.g., locals() from the caller).
    extra_kwargs : dict
        Dict of **kwargs passed to the caller.

    Raises
    ------
    ValueError
        If any disallowed parameters are set when `keyword` is not None.
    """
    if keyword is None:
        return  # nothing to check

    # 1) Named arguments (explicit parameters from the function signature).
    candidates = {
        k: v
        for k, v in all_args.items()
        if k not in allowed_with_keyword | {"keyword", "kwargs"}
    }

    # 2) Extra keyword arguments (**kwargs).
    extra = {k: v for k, v in extra_kwargs.items() if k not in allowed_with_keyword}

    # 3) Collect any that are non-None (i.e. actually set by the caller).
    disallowed = {k for k, v in candidates.items() if v is not None}
    disallowed |= {k for k, v in extra.items() if v is not None}

    if disallowed:
        raise ValueError(
            "When 'keyword' is used, no other filter parameters may be specified. "
            f"Got: {sorted(disallowed)}",
        )
