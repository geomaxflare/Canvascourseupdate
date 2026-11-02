# Medallion Architecture (Bronze, Silver, Gold)

### Learning outcomes

After this page, you should be able to:

- Define the purpose, contents, and quality guarantees of the bronze, silver, and gold layers.
- Write idempotent, incremental loads between layers and explain why idempotency matters.
- Specify data quality rules for a real dataset and decide whether violating rows should be dropped, corrected, or quarantined.
- Evaluate when the medallion pattern adds value and when it adds only cost.

### Required reading

Reis and Housley, *Fundamentals of Data Engineering*, Chapter 3, "Designing Good Data Architecture," on the data lakehouse, and Chapter 8, "Queries, Modeling, and Transformation," on transformations.

### The pattern

The **medallion architecture** organizes a lakehouse into layers of increasing refinement. Each layer is a set of tables with an explicit contract about what consumers can rely on.

| Layer | Contract | Typical operations | Consumers |
| --- | --- | --- | --- |
| **Bronze** | A faithful, append-only record of what each source delivered, plus ingestion metadata | Ingest; add load timestamp, source file, and batch ID; no business logic | Data engineers; reprocessing |
| **Silver** | Validated, de-duplicated, conformed records with consistent types, names, and keys | Type casting, quality rules, de-duplication, standardizing codes, joining related sources | Engineers, analysts, data scientists |
| **Gold** | Business-ready models for specific uses | Dimensional models, aggregates, metrics, features for machine learning | Analysts, BI tools, applications |

The pattern is closely related to older warehouse designs: Kimball's staging area, Inmon's integration layer, and presentation-layer data marts. What is new is that all three layers live as open table format tables on the same object storage.

### Design principles

**Bronze is immutable history.** Never edit bronze in place. Because bronze preserves exactly what arrived, every downstream table can be rebuilt if a rule turns out to be wrong. That **replayability** is the main reason to keep raw data.

**Every load must be idempotent.** Running a load twice must produce the same result as running it once. Pipelines fail and are retried; a non-idempotent load that blindly appends creates duplicates on every retry. Common techniques are overwriting a whole partition for the batch being processed, or using `MERGE` keyed on a natural or surrogate key.

**Process incrementally.** Reprocessing all history on every run becomes impractical as data grows. Incremental loads track a **watermark**, such as the latest load timestamp already processed, and handle only newer records. They must also handle **late-arriving data**: records that arrive after their time period was already processed.

**Decide what to do with bad data.** For each quality rule, decide whether a violating row is **dropped**, **corrected** (for example, standardizing a code), or **quarantined** to a separate table for review. Silently dropping data hides problems from the business, while letting it through corrupts results. Quarantining with a reason code makes the decision visible and measurable.

### Applying it to the taxi data

| Layer | Table | Rules and transformations |
| --- | --- | --- |
| Bronze | `bronze_yellow_trips` | All rows and columns as delivered, plus `_source_file` and `_loaded_at` |
| Silver | `silver_trips` | Keep trips whose pickup falls in the file's month; dropoff after pickup; distance between 0 and 100 miles; fare and total not negative; standardized payment type labels |
| Silver | `silver_trips_quarantine` | Rejected rows with a `reject_reason` |
| Gold | `gold_daily_borough_revenue` | Trips, revenue, and average fare per mile by day and pickup borough, joined to the taxi zone lookup |

The silver step can be expressed as a single, rerunnable SQL statement:

```sql
CREATE OR REPLACE TABLE silver_trips AS
SELECT
  VendorID AS vendor_id,
  tpep_pickup_datetime AS pickup_ts,
  tpep_dropoff_datetime AS dropoff_ts,
  PULocationID AS pickup_zone_id,
  DOLocationID AS dropoff_zone_id,
  trip_distance,
  fare_amount,
  total_amount,
  CASE payment_type WHEN 1 THEN 'Credit card' WHEN 2 THEN 'Cash'
       WHEN 3 THEN 'No charge' WHEN 4 THEN 'Dispute' ELSE 'Other or unknown' END AS payment_type
FROM bronze_yellow_trips
WHERE tpep_dropoff_datetime > tpep_pickup_datetime
  AND trip_distance > 0 AND trip_distance < 100
  AND fare_amount >= 0 AND total_amount >= 0
  AND date_trunc('month', tpep_pickup_datetime)
      = make_date(CAST(regexp_extract(_source_file, '(\d{4})-(\d{2})', 1) AS INT),
                  CAST(regexp_extract(_source_file, '(\d{4})-(\d{2})', 2) AS INT), 1);
```

Because it uses `CREATE OR REPLACE`, rerunning it produces the same table every time, which makes it idempotent at the cost of reprocessing everything. Making it incremental is one of the analysis questions below.

### Anti-patterns

- **Gold as a copy of silver:** a gold table with the same grain and columns as its silver source adds storage and maintenance with no value.
- **Business logic in bronze:** filtering or transforming on ingestion destroys replayability.
- **Unbounded layers:** adding "platinum," "diamond," and so on usually signals unclear contracts rather than a real need.
- **No ownership per layer:** each table needs an owner responsible for its contract and its quality tests.

### Lab 1.4: A three-layer pipeline in DuckDB

1. Create a persistent database (`duckdb taxi.duckdb`) and load bronze from all three monthly files, adding ingestion metadata:

```sql
CREATE OR REPLACE TABLE bronze_yellow_trips AS
SELECT *, filename AS _source_file, now() AS _loaded_at
FROM read_parquet('yellow_tripdata_2024-0*.parquet', filename = true);
```

2. Build `silver_trips` using the statement above, and build `silver_trips_quarantine` holding every bronze row that fails a rule, with a `reject_reason` column naming the first rule it failed.
3. Verify that bronze row count equals silver plus quarantine. If it does not, find out why.
4. Load `taxi_zone_lookup.csv` and build `gold_daily_borough_revenue` with trips, total revenue, and revenue per mile by pickup date and borough.
5. Run your entire pipeline a second time and confirm that every row count is unchanged.

**Submit:** your SQL script, a table of row counts per layer, the number of rows rejected by each rule, and a one-paragraph data quality summary written for a non-technical manager.

### Analysis questions

1. Rewrite the silver load so that it processes only bronze rows loaded since the last run, using a watermark. How would your design handle a corrected file for January delivered in April?
2. For each silver rule, argue whether violating rows should be dropped, corrected, or quarantined, and who in the organization should make that decision.
3. A small department has one data source and one dashboard. Argue for or against implementing all three medallion layers, considering cost, complexity, and risk.

### Key terms

Medallion architecture, bronze, silver, gold, layer contract, replayability, idempotency, incremental load, watermark, late-arriving data, quarantine, reject reason, data ownership.
