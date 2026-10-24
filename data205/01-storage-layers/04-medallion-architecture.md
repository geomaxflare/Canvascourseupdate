# Medallion Architecture (Bronze, Silver, Gold)

The **medallion architecture** is a common way to organize a lakehouse into three layers. Data moves from raw to refined, and each layer has a clear purpose and level of trust.

### The three layers

| Layer | Contents | Typical work | Main users |
| --- | --- | --- | --- |
| **Bronze** (raw) | Data exactly as received from source systems, plus load details such as the file name and load time | Ingest only; keep everything, change nothing | Data engineers |
| **Silver** (cleaned) | Validated, de-duplicated, standardized data with consistent types and names | Clean, conform, join related sources | Data engineers, analysts, data scientists |
| **Gold** (business-ready) | Aggregated tables and dimensional models built for specific reporting needs | Model, aggregate, apply business rules | Analysts, dashboards, executives |

### Following one dataset through

Using the census data from earlier courses:

1. **Bronze:** the downloaded CSV, loaded as-is, garbled header (`ï»¿State_County`) and all.
2. **Silver:** header fixed, `State_County` split into `state` and `county`, state names standardized to two-letter codes, duplicate county records removed.
3. **Gold:** a `state_population` summary table and a county dimension ready for a Power BI dashboard.

### Why use layers?

- **Recoverability:** because bronze keeps the original data, silver and gold can always be rebuilt if a cleaning rule turns out to be wrong.
- **Clear trust levels:** users know that gold data has passed every check, while bronze has passed none.
- **Lineage:** each layer documents one stage of the journey from source to report.
- **Reuse:** many gold tables can be built from the same silver data without repeating the cleaning.

### Check yourself

1. In which layer would you remove duplicate records? In which would you calculate monthly sales totals?
2. Why should bronze data never be edited in place?
3. Map the SQL data cleaning exercise from DATA 110 to the three layers.
