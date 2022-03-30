# probis Example Usage Usage

## Occurrence
Input Parameter Details

| Input param     | Data Type | Description              |
| --------------- | --------- | ------------------------ |
| scientificname  | String    | Scientific name. Leave empty to include all taxa. |
| taxonid         | String    | Taxon AphiaID                   |

```
from pyobis import occurrence
occurrence.search(scientificname='Mola mola')
```