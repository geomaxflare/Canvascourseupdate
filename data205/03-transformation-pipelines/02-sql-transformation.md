# SQL as the Transformation Language

In an ELT pipeline, most transformations are written in **SQL**. You already know SQL from querying data. In a pipeline, each transformation is a `SELECT` statement whose result becomes a new table or view.

### Why SQL?

- **Declarative:** you describe *what* result you want, and the engine decides *how* to compute it efficiently.
- **Widely known:** analysts, engineers, and many business users can read it.
- **Runs where the data lives:** the warehouse does the work, so no data needs to be moved out.
- **Portable skills:** the core language is similar across platforms.

### Common transformation patterns

| Task | SQL tools |
| --- | --- |
| Clean and standardize | `TRIM`, `UPPER`, `CAST`, `COALESCE`, `CASE` |
| Remove duplicates | `DISTINCT`, `ROW_NUMBER()` with a filter |
| Combine sources | `JOIN`, `UNION ALL` |
| Summarize | `GROUP BY` with `SUM`, `COUNT`, `AVG` |
| Calculate across rows | Window functions such as `LAG`, `RANK`, running totals |

### Example: bronze to silver

This turns raw census rows into a clean silver table, keeping one row per county:

```sql
CREATE TABLE silver_county AS
WITH ranked AS (
  SELECT
    TRIM(SUBSTRING_INDEX(state_county, ',', -1)) AS state,
    TRIM(SUBSTRING_INDEX(state_county, ',', 1))  AS county,
    CAST(population AS UNSIGNED)                 AS population,
    CONCAT(state_code, '-', county_code)         AS unique_county_code,
    ROW_NUMBER() OVER (
      PARTITION BY state_code, county_code
      ORDER BY loaded_at DESC)                   AS row_num
  FROM bronze_census
)
SELECT state, county, population, unique_county_code
FROM ranked
WHERE row_num = 1;   -- keep only the newest copy of each county
```

### Building in steps

Large transformations are easier to read and test when split into small steps. **Common table expressions** (`WITH ... AS`) name each step, and each step can later become its own model. A good rule: one transformation, one purpose.

### Check yourself

1. What does "declarative" mean, and why does it help the database run queries efficiently?
2. In the example, what does `ROW_NUMBER()` with `row_num = 1` accomplish?
3. Rewrite one of your SQL cleaning steps from DATA 110 as a `CREATE TABLE ... AS SELECT` statement.
