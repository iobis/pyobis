# pyobis Example Usage

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1z5YE1R10UyD0IN9dZovDzrf-_4AT60Xe?usp=sharing)

Click this badge to open these examples directly in Google Colab Jupyter Notebook.
## Occurrence
*Using occurrences.search: to find occurrences based on scientificname, or for all taxa if left blank.*

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
print(res["results"])
print(pd.DataFrame(res["results"]))
```
**Expected Output**
```
Out [1]:
[{'infraphylum': 'Gnathostomata', 'date_year': 2012, 'scientificNameID': 'urn:lsid:marinespecies.org:taxname:127405', 'scientificName': 'Mola mola', 'individualCount': '1', 'associatedReferences': '[{"crossref":{"citeinfo":{"origin":"Gatzke J, Khan C, Henry A, Cole T, Duley P","pubdate":"2013", ..............
}]

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
*Using occurrences.get(): to get record with id*

id parameter is Occurrence UUID, which is returned as "id" from occurrences.search()

*Example Usage*
```
from pyobis import occurrences
res=occurrences.get(id='00009261-7e82-4558-afd3-31b9fa3a7900')
print(res["results"])
print(pd.DataFrame(res["results"]))
```
**Expected Output**
```
Out [1]:
[{'type': 'Event', 'class': 'Actinopteri', 'genus': 'Mola', 'order': 'Tetraodontiformes', 'family': 'Molidae', 'phylum': 'Chordata', 'kingdom': 'Animalia', 'license': 'http://creativecommons.org/licenses/by-nc/4.0/', 'modified': '2022-02-03 15:29:13', 'datasetID': '513', ...............
}]

Out [2]:
    type        class  ...   dna                                             source
0  Event  Actinopteri  ...  None  {'type': 'Event', 'class': 'Actinopterygii', '...

[1 rows x 84 columns]
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