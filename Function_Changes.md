# New tasks to do
Tasks completed are striken-through ~~like this~~
+ ~~improve MoF accessiblity~~
+ Create tutorial usage of occurrence module
+ create CONTRIBUTING.md
+ update readme badges and/or review coveralls coverage plus reviewing tests
+ fix setup.py
+ Use CI push to PyPI
+ demo jupyter notebooks
+ create visualization module (or separate package)

## Proposed module/function changes
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

|pyobis.taxa|                    |
|-----------|--------------------|
|taxon/{scientificname}| taxa.search(scientificname, **kwargs). It requires only scientificname |
|taxon/{id}| taxa.taxon(id, **kwargs). It requires only TaxonID |
|taxon/annotations|taxa.annotations(scientificname, **kwargs). It requires only scientific name |

--------------------
## Changes made
|pyobis.occurrences as occ|          |
|-------------------------|----------|
|occurrences/point/{x}/{y}|occ.point(x,y,scientificname,...,**kwargs) {updated}|
|occurrences/centroid|occ.centroid(scientificname,...,**kwargs) {updated}|
|occurrences/points|occ.getpoints(scientificname,...,**kwargs) {updated}|
|occurrences/grid/{precision}|occ.grid(precision =None, geojson=False, **kwargs)|
|*If GeoJSON=1, then GeoJSON response, if 0 then KML response.*||
|occurrences/tile/{x}/{y}/{z}|occ.tile(x,y,z,scientificname,mvt=1...,**kwargs)|
|*If mvt=1, return response as MVT, if mvt =0, return response as GeoJSON*||

## Proposed changes
*All done!*