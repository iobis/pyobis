from ..obisutils import *

class ObisDownload(object):
    """
    ObisDownload class

    methods:

    - uuid: get uuid for the download
    - status: get download status
    - fetch: retrieve the download
    """
    def __init__(self, uuid):
        super(ObisDownload, self).__init__()
        self.uuid = uuid
        self.file_path = None

    def __repr__(self):
        return '<OBIS Occurrence Download>\n  uuid: ' + self.uuid

    def status(self, **kwargs):
        url = obis_baseurl + 'download/%s/status' % str(self.uuid)
        res = obis_GET(url, {}, 'text/x-json;charset=UTF-8', **kwargs)
        return res

    def fetch(self, path = ".", **kwargs):
        url = obis_baseurl + 'download/%s' % str(self.uuid)
        path = "%s/%s.zip" % (path, self.uuid)
        self.file_path = path
        obis_write_disk(url, path, 'content=type', **kwargs)
        print("On disk at " + path)
        return path


def download(scientificname=None, aphiaid=None, obisid=None, resourceid=None,
    startdate=None, enddate=None, startdepth=None, enddepth=None,
    geometry=None, year=None, qc=None, fields=None, **kwargs):
    '''
    Download OBIS occurrences

    :param aphiaid: [Fixnum] A obis occurrence identifier
    :param scientificname: [String,Array] One or more scientific names from the OBIS backbone. All included and
       synonym taxa are included in the search.
    :param year: [Fixnum] The 4 digit year. A year of 98 will be interpreted as AD 98. Supports range queries,
       smaller,larger (e.g., '1990,1991', whereas '1991,1990' wouldn't work)
    :param geometry: [String] Well Known Text (WKT). A WKT shape written as either POINT, LINESTRING, LINEARRING
       or POLYGON. Example of a polygon: ((30.1 10.1, 20, 20 40, 40 40, 30.1 10.1)) would be queried as http://bit.ly/1BzNwDq
    :param obisid: [Fixnum] An OBIS id. This is listed as the `id` or `valid_id` in `taxa`/`taxon` results
    :param aphiaid: [Fixnum] An Aphia id. This is listed as the `worms_id` in `taxa`/`taxon` results
    :param resourceid: [Fixnum] An resource id
    :param startdate: [Fixnum] Start date
    :param enddate: [Boolean] End date
    :param startdepth: [Fixnum] Start depth
    :param enddepth: [Boolean] End depth
    :param qc: [String] Quality control flags
    :param fields: [Array] Array of field names

    :return: An object of class ObisDownload with methods to continue accessing the data

    Usage::

        from pyobis import occurrences as occ

        # query to generate a download job
        res = occ.download(year = 2001, scientificname = 'Orcinus')

        # get the uuid for your download job
        res.uuid

        # get status of download prep
        res.status()

        # fetch file, writes to disk
        res.fetch()

        # get file path
        x.file_path

        # unzip the file
        import zipfile
        import tempfile
        import shutil
        import os

        zipf = zipfile.ZipFile(x, 'r')
        dir = tempfile.mkdtemp()
        zipf.extractall(dir)
        fpath = dir + '/' + os.listdir(dir)[0]
        zipf.close()

        # read some lines of the csv
        import csv
        with open(fpath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['genus'], row['species'])

        # cleanup
        shutil.rmtree(dir)
    '''
    url = obis_baseurl + 'occurrence/download'
    scientificname = handle_arrstr(scientificname)
    out = obis_GET(url, {'aphiaid': aphiaid, 'obisid': obisid,
        'resourceid': resourceid, 'scientificname': scientificname,
        'startdate': startdate, 'enddate': enddate, 'startdepth': startdepth,
        'enddepth': enddepth, 'geometry': geometry, 'year': year,
        'fields': fields, 'qc': qc}, 'text/x-json;charset=UTF-8', **kwargs)
    return ObisDownload(uuid = out['uuid'])
