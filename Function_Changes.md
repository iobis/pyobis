# Proposed module/function changes
In continuation of the GSoC 2022 objective 1: Modifying API calls in the pyobis package.

## Reference:
| module to be changed | (any comments) |
|----------------------|----------------|
| API endpoint| corresponding function in module.|

## Changes already done
|pyobis.checklist|                    |
|----------------|--------------------|
|checlist/| checklist.list(scientificname, **params, **kwargs)|
|checklist/redlist| checklist.redlist(scientificname,**params, **kwargs)|
|checklist/newest|checklist.newest(scientificname, **param, **kwargs)|

|pyobis.dataset|*It has been renamed from pyobis.resource*|
|--------------|------------------------------------------|
|dataset/| dataset.search(scientificname,**params, **kwargs)|
|dataset/{id}/| dataset.get(id, **kwargs). It requires only ID|

All other functions existing previously in the resources module have been deleted, and it is renamed to dataset module.

|pyobis.nodes|                    |
|------------|--------------------|
|node/{id}| nodes.search(id, **kwargs). It requires only Node UUID|
|node/{id}/activities| nodes.activities(id, **kwargs). It requires only Node UUID|

**pyobis.groups** has become obsolete and hence proposed to be deleted.

--------------------

## Proposed changes
*Resources in the new API for which new functions/modules need to be created*

|pyobis.occurrences as occ|          |
|-------------------------|----------|
|occurrences/grid/{precision}|occ.grid(precision =None, geojson=False, **kwargs)|
|*If GeoJSON=1, then GeoJSON response, if 0 then KML response.*||
|occurrences/points|occ.getpoints(scientificname,...,**kwargs)|
|occurrences/point/{x}/{y}/{z}|occ.point(x,y,z,scientificname,...,**kwargs)|
|occurrences/tile/{x}/{y}/{z}|occ.tile(x,y,z,scientificname,mvt=1...,**kwargs)|
|*If mvt=1, return response as MVT, if mvt =0, return response as GeoJSON*||
|occurrences/centroid|occ.centroid(scientificname,...,**kwargs)|

|pyobis.taxa|                    |
|-----------|--------------------|
|taxon/{scientificname}| taxa.search(scientificname, **kwargs). It requires only scientificname|
|taxon/{id}| taxa.taxon(id, **kwargs). It requires only TaxonID|
|taxon/annotations|taxa.taxon(scientificname, **kwargs). It requires only scientific name|