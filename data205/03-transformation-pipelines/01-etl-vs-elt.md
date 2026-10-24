# ETL versus ELT

Every data pipeline does three things: **extract** data from sources, **transform** it into a useful shape, and **load** it into a destination. The order of the last two steps defines two approaches.

### ETL: Extract, Transform, Load

Data is transformed on a separate processing server *before* it is loaded into the warehouse.

```
Source systems -> [ transform on ETL server ] -> Data warehouse
```

- Grew up when warehouse storage and computing were expensive, so only clean, final data was loaded.
- Transformations often lived in specialized ETL tools.
- **Drawback:** raw data is not kept in the warehouse, so a new question or a fixed bug may mean re-extracting from the source.

### ELT: Extract, Load, Transform

Data is loaded raw into the warehouse or lakehouse first, then transformed *inside* it.

```
Source systems -> Data warehouse / lakehouse (raw) -> [ transform with SQL ] -> clean tables
```

- Made practical by cloud platforms with low-cost storage and scalable computing.
- Matches the medallion architecture: load to bronze, transform to silver and gold.
- **Advantages:** raw data is always available to rebuild from; transformations use the platform's own power; analysts can write transformations in SQL.

### Comparison

| | ETL | ELT |
| --- | --- | --- |
| Where transformation happens | Separate processing server | Inside the warehouse or lakehouse |
| Raw data kept in destination | Usually not | Yes |
| Typical language | ETL tool or general programming | Mostly SQL |
| Good fit when | Data must be masked or filtered before it lands, or the destination is limited | Cloud platform with plenty of storage and computing |

ETL is not obsolete. If sensitive data, such as Social Security numbers, must never be stored in the warehouse, it may need to be removed *before* loading.

### Check yourself

1. Why did ETL make sense when warehouse storage was expensive?
2. How does keeping raw data help when a cleaning rule turns out to be wrong?
3. Give one situation where transforming before loading is still the better choice.
