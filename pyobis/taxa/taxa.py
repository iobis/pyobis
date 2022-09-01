"""
/taxon/ API endpoints as documented on https://api.obis.org/.
"""
from ..obisutils import OBISQueryResult, handle_arrstr, obis_baseurl, obis_GET


class TaxaQuery(OBISQueryResult):
    def __init__(self):
        """
        An TaxaQuery object for fetching Taxa records.
        """

    def search(self, scientificname=None, **kwargs):
        """
        Get taxon records.

        :param scientificname: [String,Array] One or more scientific names from the
            OBIS backbone. All included and synonym taxa are included in the search

        :return: A dictionary

        Usage::

            from pyobis.taxa import TaxaQuery
            taxa = TaxaQuery()
            taxa.search(scientificname = 'Mola mola')
            taxa.search(scientificname=['Mola mola','Abra alba'])
        """

        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.url = obis_baseurl + "taxon/" + scientificname
        OBISQueryResult.args = {"scientificname": scientificname}
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        return out

    def taxon(self, id, **kwargs):
        """
        Get taxon by ID

        :param id: [Fixnum] An OBIS taxon identifier

        :return: A dictionary

        Usage::

            from pyobis.taxa import TaxaQuery
            taxa = TaxaQuery()
            taxa.taxon(545439)
            taxa.taxon(402913)
            taxa.taxon(406296)
            taxa.taxon(415282)
        """
        OBISQueryResult.url = obis_baseurl + "taxon/" + str(id)
        OBISQueryResult.args = {}
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        return out

    def annotations(self, scientificname, **kwargs):
        """
        Get scientific name annotations by the WoRMS team.

        :param scientificname: [String] Scientific name. Leave empty to include all taxa.
        :return: A dictionary

        Usage::

            from pyobis.taxa import TaxaQuery
            taxa = TaxaQuery()
            taxa.annotations(scientificname="Abra")
        """
        OBISQueryResult.url = obis_baseurl + "taxon/annotations"
        scientificname = handle_arrstr(scientificname)
        OBISQueryResult.args = {"scientificname": scientificname}
        out = obis_GET(
            OBISQueryResult.url,
            OBISQueryResult.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        return out
