# Open Table Formats (Delta Lake, Iceberg)

A folder of Parquet files is not a table. If two jobs write to it at once, or a load fails halfway through, readers can see broken or partial data. **Open table formats** solve this by adding a metadata layer that makes files in object storage behave like a reliable database table.

### How they work

An open table format keeps a **transaction log** (or metadata files) next to the data files. The log records exactly which files make up the table at each point in time. Readers consult the log, never just "whatever files are in the folder."

The two most common formats are **Delta Lake** and **Apache Iceberg**. Both store data in Parquet and add similar capabilities.

### What they add

| Capability | What it means for analysts |
| --- | --- |
| **ACID transactions** | A load either fully succeeds or leaves the table unchanged. No half-written tables. |
| **Updates, deletes, and merges** | Rows can be changed or removed, for example to fix errors or honor a deletion request, without rewriting the whole table by hand. |
| **Schema enforcement and evolution** | Bad data with the wrong columns is rejected, while planned changes (adding a column) are allowed. |
| **Time travel** | Query the table as it looked at an earlier version or time, which helps with audits and recovering from mistakes. |
| **Open and engine-neutral** | Spark, SQL engines, and BI tools can all read the same table. |

### Example: time travel

```sql
-- Delta Lake syntax: the table as it was before yesterday's bad load
SELECT state, SUM(population)
FROM census_county VERSION AS OF 12
GROUP BY state;
```

### The lakehouse

Combining low-cost object storage, open table formats, and SQL engines produces what is often called a **lakehouse**: the flexibility and cost of a data lake with the reliability and performance of a data warehouse.

### Check yourself

1. Why is a plain folder of Parquet files risky when two processes write to it at the same time?
2. Describe a situation where time travel would help an analyst.
3. What does the term *lakehouse* combine?
