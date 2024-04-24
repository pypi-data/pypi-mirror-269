# vlgi-datasets

## Overview

Repositiory with custom kedro datasets

## How to use

In code:
```python
from kedro.io import DataCatalog
from vlgi_datasets import PostgresTableUpsertDataset

io = DataCatalog(
    {
        "asset": PostgresTableUpsertDataset(
            table_name="assets",
            credentials={"con": "myconnectionstring"},
            save_args={"if_exists": "append", "constraint": "assets_pkey"},
        ),
    }
)
```

In catalog.yml:
```yaml
asset:
  type: vlgi_datasets.PostgresTableUpsertDataset
  table_name: assets
  credentials:
    con: myconnectionstring
  save_args:
    if_exists: append
    constraint: assets_pkey
```
