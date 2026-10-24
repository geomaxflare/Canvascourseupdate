# Partitioning and Query Performance

The fastest data to process is data you never read. **Partitioning** organizes data on storage so that queries can skip whatever they do not need.

### Partitioning data on storage

A partitioned table stores its files in folders named by the value of one or more columns:

```
sales/
  year=2025/month=11/part-0001.parquet
  year=2025/month=12/part-0001.parquet
  year=2026/month=01/part-0001.parquet
```

A query filtering on `year = 2026 AND month = 1` reads only one folder. Skipping the others is called **partition pruning**.

### Choosing a partition column

| Good partition column | Poor partition column |
| --- | --- |
| Commonly used in filters, such as date | Rarely filtered on |
| Moderate number of distinct values, such as months or regions | Very many values, such as customer ID, which creates millions of tiny folders |
| Spreads data fairly evenly | One value holds most of the data (*skew*) |

### The small files problem

Thousands of tiny files are slow, because opening each file has a fixed cost. Aim for fewer, larger files (often in the range of hundreds of megabytes). Table formats such as Delta Lake and Iceberg include **compaction** commands that combine small files.

### Other performance tools

- **Column pruning:** with columnar formats, read only the columns a query uses.
- **Predicate pushdown:** use min and max statistics stored in Parquet files to skip chunks that cannot match a filter.
- **Clustering or sorting:** store related values near each other so more chunks can be skipped.
- **Data skew:** if one key holds far more rows than others, one task does most of the work while the rest wait. Spotting skew is an important tuning skill.
- **Broadcast joins:** when one side of a join is small (like a dimension table), copy it to every machine instead of shuffling the large side.

### Check yourself

1. A table is partitioned by `year` and `month`. Which folders does a query for December 2025 read?
2. Why is partitioning by customer ID usually a bad idea?
3. Why are broadcast joins a good fit for star schemas?
