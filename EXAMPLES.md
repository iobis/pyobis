# pyobis Example Usage

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1z5YE1R10UyD0IN9dZovDzrf-_4AT60Xe?usp=sharing)

Click this badge to open these examples directly in Google Colab Jupyter Notebook.
## Occurrence

----
*Using occurrences.search(): to find occurrences based on scientificname, or for all taxa if left blank.*

Input Parameter Details

| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID                   |
| datasetid       | String| Dataset UUID|
|startdate|String|Start date formatted as YYYY-MM-DD|
|enddate|String|End date formatted as YYYY-MM-DD|
|startdepth|Integer|Start depth, in meters|
|enddepth| Integer|End depth, in meters|
|geometry|String|Geometry, formatted as WKT or GeoHash|
|flags| String|Comma separated list of quality flags that need to be set|
|mof|Boolean|True/False, Include MeasurementOrfact records|
|fields|String| Fields to be included in the result set|
|extensions|String|Extensions to include (e.g. MeasurementOrFact, DNADerivedData)|
|hasextensions|String|Extensions that need to be present (e.g. MeasurementOrFact, DNADerivedData)|

Example Usage
```
from pyobis import occurrences
res=occurrences.search(scientificname='Mola mola')
print(res)
print(pd.DataFrame(res["results"]))
```
**Expected Output**
```
Out [1]:
{'infraphylum': 'Gnathostomata', 'date_year': 2012, 'scientificNameID': 'urn:lsid:marinespecies.org:taxname:127405', 'scientificName': 'Mola mola', 'individualCount': '1', 'associatedReferences': '[{"crossref":{"citeinfo":{"origin":"Gatzke J, Khan C, Henry A, Cole T, Duley P","pubdate":"2013", ..............
}

Out [2]:
   infraphylum   date_year   ...  depth  country
0  Gnathostomata       2012  ...   NaN     NaN
1  Gnathostomata       2007  ...   NaN     NaN
2  Gnathostomata       2019  ...   NaN     NaN
3  Gnathostomata       1979  ...   NaN     NaN
4  Gnathostomata       2008  ...   NaN     NaN
5  Gnathostomata       2021  ...   NaN     NaN
6  Gnathostomata       2013  ...   0.0     NaN
7  Gnathostomata       2012  ...   NaN      FR
8  Gnathostomata       1980  ...   NaN     NaN
9  Gnathostomata       2012  ...   NaN      FR

[10 rows x 95 columns]
```
----
*Using occurrences.get(): to get record with id*

id parameter is Occurrence UUID, which is returned as "id" from occurrences.search()

*Example Usage*
```
from pyobis import occurrences
res=occurrences.get(id='00009261-7e82-4558-afd3-31b9fa3a7900')
print(res)
print(pd.DataFrame(res["results"]))
```
**Expected Output**
```
Out [1]:
{'type': 'Event', 'class': 'Actinopteri', 'genus': 'Mola', 'order': 'Tetraodontiformes', 'family': 'Molidae', 'phylum': 'Chordata', 'kingdom': 'Animalia', 'license': 'http://creativecommons.org/licenses/by-nc/4.0/', 'modified': '2022-02-03 15:29:13', 'datasetID': '513', ...............
}

Out [2]:
    type        class  ...   dna                                             source
0  Event  Actinopteri  ...  None  {'type': 'Event', 'class': 'Actinopterygii', '...

[1 rows x 84 columns]
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Occurrence/).

----
*Using occurrences.grid(): to Fetch gridded occurrences as GeoJSON or KML.*
| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| precision       | Integer   | Geohash precision        |
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID                   |
| datasetid       | String| Dataset UUID|
|startdate|String|Start date formatted as YYYY-MM-DD|
|enddate|String|End date formatted as YYYY-MM-DD|
|startdepth|Integer|Start depth, in meters|
|enddepth| Integer|End depth, in meters|
|geometry|String|Geometry, formatted as WKT or GeoHash|
|flags| String|Comma separated list of quality flags that need to be set|
|redlist | Boolean| Red List species only, True/False.|
| hab | Boolean | HAB species only, true/false.|
| event|String| Include pure event records (include) or get pure event records exclusively (true).|
| exclude| String| Comma separated list of quality flags to be excluded.|

*Example Usage*
```
from pyobis import occurrences
res=occurrences.grid(precision=1, geojson=True, scientificname='Abra alba')
print(res)
print(pd.DataFrame(res))
```
**Expected Output**
```
Out [1]:
{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[0, 45], [45, 45], [45, 90], [0, 90], [0, 45]]]}, 'properties': {'n': 41878}}, {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[-45, 45], [0, 45], [0, 90], [-45, 90], [-45, 45]]]}, 'properties': {'n': 18277}}, {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[0, 0], [45, 0], [45, 45], [0, 45], [0, 0]]]}, 'properties': {'n': 662}}, {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[-45, 0], [0, 0], [0, 45], [-45, 45], [-45, 0]]]}, 'properties': {'n': 81}}, {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[-90, 0], [-45, 0], [-45, 45], [-90, 45], [-90, 0]]]}, 'properties': {'n': 1}}]}

Out [2]:
                type                                           features
0  FeatureCollection  {'type': 'Feature', 'geometry': {'type': 'Poly...
1  FeatureCollection  {'type': 'Feature', 'geometry': {'type': 'Poly...
2  FeatureCollection  {'type': 'Feature', 'geometry': {'type': 'Poly...
3  FeatureCollection  {'type': 'Feature', 'geometry': {'type': 'Poly...
4  FeatureCollection  {'type': 'Feature', 'geometry': {'type': 'Poly...
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Occurrence/).

----
*Using occurrences.getpoints(): to Fetch point occurrences as GeoJSON (aggregated to Geohash precision 8)*
| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID                   |
| datasetid       | String| Dataset UUID|
| nodeid       | String| Node UUID|
|startdate|String|Start date formatted as YYYY-MM-DD|
|enddate|String|End date formatted as YYYY-MM-DD|
|startdepth|Integer|Start depth, in meters|
|enddepth| Integer|End depth, in meters|
|geometry|String|Geometry, formatted as WKT or GeoHash|
|redlist | Boolean| Red List species only, True/False.|
| hab | Boolean | HAB species only, true/false.|
| event|String| Include pure event records (include) or get pure event records exclusively (true).|
| flags|String| Comma separated list of quality flags which need to be set.|
| exclude| String| Comma separated list of quality flags to be excluded.|

*Example Usage*
```
from pyobis import occurrences
res=occurrences.getpoints(scientificname = ['Mola mola','Abra alba'])
print(res)
print(pd.DataFrame(res))
```
**Expected Output**
```
Out [1]:
{'type': 'MultiPoint', 'coordinates':[[4.104595184326172, 51.50897026062012], [4.085025787353516, 51.5244197845459], [4.082965850830078, 51.5218448638916], 
...
...
[4.080219268798828, 51.52287483215332], [4.077129364013672, 51.5218448638916], [4.078502655029297, 51.521501541137695], [4.023571014404297, 51.62123680114746], [4.018421173095703, 51.620378494262695], [4.000911712646484, 51.614885330200195]]}

Out [2]:
           type                               coordinates
0     MultiPoint   [10.318737030029297, 56.15464210510254]
1     MultiPoint  [10.289554595947266, 56.092844009399414]
2     MultiPoint   [-3.8804054260253906, 48.8027286529541]
3     MultiPoint  [10.246295928955078, 56.114816665649414]
4     MultiPoint  [10.245609283447266, 56.136274337768555]
...          ...                                       ...
9995  MultiPoint     [4.071636199951172, 51.5079402923584]
9996  MultiPoint   [4.071636199951172, 51.507768630981445]
9997  MultiPoint    [4.023571014404297, 51.62123680114746]
9998  MultiPoint   [4.018421173095703, 51.620378494262695]
9999  MultiPoint   [4.000911712646484, 51.614885330200195]

[10000 rows x 2 columns]
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Occurrence/).

---- 
*Using occurrences.point(): to Fetch point occurrences for a location (with Geohash precision 8 or variable Geohash precision) as GeoJSON.*
| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| x               | float     | latitudes of a location  |
| y | float| laongitude of a location|
|z| float| zoom level, if present then variable Geohash precision, if absent then precision 8|
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID        |
| datasetid       | String| Dataset UUID|
| nodeid       | String| Node UUID|
|startdate|String|Start date formatted as YYYY-MM-DD|
|enddate|String|End date formatted as YYYY-MM-DD|
|startdepth|Integer|Start depth, in meters|
|enddepth| Integer|End depth, in meters|
|geometry|String|Geometry, formatted as WKT or GeoHash|
|redlist | Boolean| Red List species only, True/False.|
| hab | Boolean | HAB species only, true/false.|
|wrims| boolean| WRiMS species only, True/False.|
| event|String| Include pure event records (include) or get pure event records exclusively (true).|
| flags|String| Comma separated list of quality flags which need to be set.|
| exclude| String| Comma separated list of quality flags to be excluded.|

*Example Usage*
```
from pyobis import occurrences
res=occurrences.point(x=1.77,y=54.22,scientificname = 'Mola mola')
print(res)
print(pd.DataFrame(res))
```
**Expected Output**
```
Out [1]:
{'total': 0, 'results': []}

Out [2]:
Empty DataFrame
Columns: [total, results]
Index: [] 
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Occurrence/).

---- 
*Using occurrences.tile(): to Fetch point occurrences for a tile (aggregated using variable Geohash precision based on zoom level) as GeoJSON or MVT.*
| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| x               | float     | latitudes of a location  |
| y | float| laongitude of a location|
|z| float| zoom level|
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID        |
| datasetid       | String| Dataset UUID|
| nodeid       | String| Node UUID|
|startdate|String|Start date formatted as YYYY-MM-DD|
|enddate|String|End date formatted as YYYY-MM-DD|
|startdepth|Integer|Start depth, in meters|
|enddepth| Integer|End depth, in meters|
|geometry|String|Geometry, formatted as WKT or GeoHash|
|redlist | Boolean| Red List species only, True/False.|
| hab | Boolean | HAB species only, true/false.|
|wrims| boolean| WRiMS species only, True/False.|
| event|String| Include pure event records (include) or get pure event records exclusively (true).|
| flags|String| Comma separated list of quality flags which need to be set.|
| exclude| String| Comma separated list of quality flags to be excluded.|

*Example Usage*
```
from pyobis import occurrences
res=occurrences.tile(x=1.77,y=52.26,z=0.5,mvt=0, scientificname = 'Mola mola')
print(res)
print(pd.DataFrame(res))
```
**Expected Output**
```
Out [1]:
{'type': 'MultiPoint', 'coordinates': [[4.921875, 42.890625], [-68.203125, 42.890625], [-72.421875, 40.078125], [-71.015625, 40.078125], [-69.609375, 42.890625], [3.515625, 42.890625], [-69.609375, 40.078125], [-66.796875, 42.890625],  
...
...
44.296875], [-145.546875, 42.890625], [-146.953125, 44.296875], [-158.203125, 21.796875], [-9.140625, -2.109375], [-9.140625, -23.203125], [-90.703125, -0.703125], [-92.109375, -0.703125], [-179.296875, -44.296875]]}

Out [2]:
           type                coordinates
0    MultiPoint      [4.921875, 42.890625]
1    MultiPoint    [-68.203125, 42.890625]
2    MultiPoint    [-72.421875, 40.078125]
3    MultiPoint    [-71.015625, 40.078125]
4    MultiPoint    [-69.609375, 42.890625]
..          ...                        ...
510  MultiPoint     [-9.140625, -2.109375]
511  MultiPoint    [-9.140625, -23.203125]
512  MultiPoint    [-90.703125, -0.703125]
513  MultiPoint    [-92.109375, -0.703125]
514  MultiPoint  [-179.296875, -44.296875]

[515 rows x 2 columns]
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Occurrence/).

---- 
*Using occurrences.centroid(): to Determine the centroid for a selection of occurrence records.*
| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID        |
| datasetid       | String| Dataset UUID|
| nodeid       | String| Node UUID|
|startdate|String|Start date formatted as YYYY-MM-DD|
|enddate|String|End date formatted as YYYY-MM-DD|
|startdepth|Integer|Start depth, in meters|
|enddepth| Integer|End depth, in meters|
|geometry|String|Geometry, formatted as WKT or GeoHash|
|redlist | Boolean| Red List species only, True/False.|
| hab | Boolean | HAB species only, true/false.|
|wrims| boolean| WRiMS species only, True/False.|
| event|String| Include pure event records (include) or get pure event records exclusively (true).|
| flags|String| Comma separated list of quality flags which need to be set.|
| exclude| String| Comma separated list of quality flags to be excluded.|

*Example Usage*
```
from pyobis import occurrences
res=occurrences.centroid(scientificname = 'Mola mola')
print(res)
```
**Expected Output**
```
Out [1]:
{'lat': 39.92252136065221, 'lon': -37.25194273118425}
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Occurrence/).

## Taxa
*Using taxa.search()*: Get taxon records.
Input Parameter Details

| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |

Example Usage
```
from pyobis import taxa
res=taxa.search(scientificname='Abra')
print(res["results"])
print(pd.DataFrame(res["results"]))
```
**Expected Output**
```
Out [1]:
[{'type': 'Event', 'class': 'Actinopteri', 'genus': 'Mola', 'order': 'Tetraodontiformes', 'family': 'Molidae', 'phylum': 'Chordata', 'kingdom': 'Animalia', 'license': 'http://creativecommons.org/licenses/by-nc/4.0/', 'modified': '2022-02-03 15:29:13', 'datasetID': '513', 'eventDate': '2012-06-21T16:14:47', 'eventTime': '20:14:47Z', 'taxonRank': 'Species', 'waterBody': 'North Atlantic Ocean', ............
}]

Out [2]:
  scientificName scientificNameAuthorship  ...  familyid  genusid
0           Abra            Lamarck, 1818  ...      1781   138474

[1 rows x 31 columns]
```
*Using taxa.taxon()*: Get taxon records.

| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| id              | integer   | Taxon AphiaID (it is returned as "taxonID" in search results)|

*Example Usage*
```
from pyobis import taxa
res=taxa.taxon(id=138474)
print(res["results"])
print(pd.DataFrame(res["results"]))
```

**Expected Output**
```
Out [1]:
[{'scientificName': 'Abra', 'scientificNameAuthorship': 'Lamarck, 1818', 'taxonID': 138474, 'ncbi_id': 121180, 'taxonRank': 'Genus', 'taxonomicStatus': 'accepted', 'acceptedNameUsage': 'Abra', 'acceptedNameUsageID': 138474, 'is_marine': True, 'kingdom': 'Animalia', 'phylum': 'Mollusca', 'class': 'Bivalvia', 'subclass': 'Autobranchia', 'infraclass': 'Heteroconchia',...........
}]

Out [2]:
  scientificName scientificNameAuthorship  ...  familyid  genusid
0           Abra            Lamarck, 1818  ...      1781   138474

[1 rows x 31 columns]
```

*Using taxa.annotations()* Get scientific name annotations by the WoRMS team.

| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| scientificname  | String    | Scientific name. Leave empty to include all taxa.|

*Example Usage*
```
from pyobis import taxa
res=taxa.annotations(scientificname="Egg")
print(res["results"])
print(pd.DataFrame(res["results"]))
```

**Expected Output**
```
Out [1]:
[{'scientificname': 'Egg', 'annotation_type': 'Black: no biota', 'annotation_comment': None, 'annotation_resolved_aphiaid': None, 'scientificnameid': 'CYCLOPS', 'phylum': None, 'class': None, 'order': None, 'family': None, 'genus': None
}]

Out [2]:
  scientificname  annotation_type annotation_comment  ... order family genus
0            Egg  Black: no biota               None  ...  None   None  None

[1 rows x 10 columns]
```
API Response details can be found here [OBIS v3 API](https://api.obis.org/#/Taxon/).
