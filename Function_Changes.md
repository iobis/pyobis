# Proposed module/function changes
In continuation of the GSoC 2022 objective 1: Modifying API calls in the pyobis package.

*Modulus for which resource is missing in the new API:*\
`pyobis/resources` and `pyobis/groups`\
*Resources in the new API for which new functions/modules need to be created:*\

|pyobis.occurrences as occ|          |
|-------------------------|----------|
|occurrences/grid/{precision}|occ.grid(precision =None, geojson=False, **kwargs)|
|*If GeoJSON=1, then GeoJSON response, if 0 then KML response.*||
|occurrences/points|occ.getpoints(scientificname,...,**kwargs)|
|occurrences/point/{x}/{y}/{z}|occ.point(x,y,z,scientificname,...,**kwargs)|
|occurrences/tile/{x}/{y}/{z}|occ.tile(x,y,z,scientificname,mvt=1...,**kwargs)|
|*If mvt=1, return response as MVT, if mvt =0, return response as GeoJSON*||
|occurrences/centroid|occ.centroid(scientificname,...,**kwargs)|
|pyobis.
