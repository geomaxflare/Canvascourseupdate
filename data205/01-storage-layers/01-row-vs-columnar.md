# Row versus Columnar Storage; Parquet

### Learning outcomes

After this page, you should be able to:

- Explain why storage layout, not processing speed, usually dominates the cost of analytical queries.
- Estimate how much data a row store and a column store must read for a given query.
- Describe the structure of a Parquet file and how engines use its metadata to skip data.
- Choose between Parquet, ORC, Avro, and CSV for a given workload and justify the choice.

### Required reading

Reis and Housley, *Fundamentals of Data Engineering*, Chapter 6, "Storage," sections on file formats, serialization, and row versus columnar storage.

### Why layout matters

Analytical queries typically scan millions or billions of rows but touch only a handful of columns. A query such as "average fare by month for 2024" needs two fields out of the nineteen in a taxi trip record. The time to answer it is dominated by **I/O**: how many bytes must move from disk or the network into memory. CPUs can aggregate data far faster than storage can deliver it, so the most effective optimization is simply to read less.

### Two physical layouts

A **row-oriented** layout (sometimes called the N-ary storage model) stores each record's values contiguously. CSV files and the storage engines of transactional databases such as MySQL's InnoDB use this layout. It suits workloads that insert, update, or fetch *whole records*, such as saving an order or loading a customer profile, because one record is one contiguous read or write.

A **columnar** layout (the decomposition storage model) stores each column's values contiguously. A query reads only the columns it references, a technique called **projection pushdown** or column pruning.

Consider a table of 3,000,000 trips with 19 columns averaging 8 bytes each (about 456 MB uncompressed). The query below references 2 columns:

```sql
SELECT date_trunc('month', tpep_pickup_datetime) AS month,
       AVG(fare_amount) AS avg_fare
FROM trips
GROUP BY 1;
```

| Layout | Data that must be read | Approximate size |
| --- | --- | --- |
| Row-oriented | Every column of every row | 456 MB |
| Columnar, uncompressed | 2 of 19 columns | 48 MB |
| Columnar, encoded and compressed | 2 columns after encoding | often well under 20 MB |

The columnar store reads roughly a tenth of the data before compression is even considered, and compression widens the gap further.

### Why columns compress well

Values in a single column share a type and often a narrow range of values, which makes them highly compressible. Columnar formats apply lightweight **encodings** before general-purpose compression:

| Encoding | How it works | Works well for |
| --- | --- | --- |
| **Dictionary** | Store each distinct value once; replace values with small integer codes | Low-cardinality text such as `payment_type`, borough, or state |
| **Run-length (RLE)** | Store a value and how many times it repeats | Sorted or clustered columns, such as a date column in time order |
| **Bit-packing** | Store small integers in only as many bits as needed | Dictionary codes, flags, small counts |
| **Delta** | Store differences between consecutive values | Timestamps and increasing IDs |

After encoding, a **compression codec** such as Snappy (fast, moderate ratio), ZSTD (good balance), or gzip (high ratio, slower) compresses each block. Choosing a codec trades CPU time for storage and I/O.

### Inside a Parquet file

**Apache Parquet** is the dominant open columnar format for analytics. Its structure is hierarchical:

| Level | What it is | Purpose |
| --- | --- | --- |
| **File** | Begins and ends with the marker `PAR1` | Self-contained unit of storage |
| **Row group** | A horizontal slice of rows, commonly sized in the range of 128 MB or about one million rows, depending on the writer | Unit of parallelism; engines can process row groups independently |
| **Column chunk** | All values of one column within a row group | Unit of column pruning |
| **Page** | A subdivision of a column chunk, typically about 1 MB | Unit of encoding and compression |
| **Footer** | Schema, the location of every column chunk, and statistics such as minimum, maximum, and null count per chunk | Read first, so the engine can plan which bytes to fetch |

Because the footer stores per-chunk minimum and maximum values, an engine evaluating `WHERE fare_amount > 200` can skip any row group whose maximum fare is below 200 without reading it. This is **predicate pushdown**, and it is most effective when data is sorted or clustered on the filtered column. Parquet also distinguishes **physical types** (how bytes are stored, such as INT64) from **logical types** (how they are interpreted, such as TIMESTAMP or DECIMAL), and it represents nested and optional fields using repetition and definition levels, an approach adapted from Google's Dremel system.

### Comparing common formats

| Format | Layout | Schema | Strengths | Typical use |
| --- | --- | --- | --- | --- |
| CSV | Row, text | None; types inferred | Human-readable, universal | Small exchanges, exports |
| Avro | Row, binary | Stored in the file header | Fast writes, strong schema evolution | Streaming, messaging, data exchange between services |
| ORC | Columnar | Stored in the file | Strong compression, built-in indexes | Hive-based ecosystems |
| Parquet | Columnar | Stored in the footer | Broad engine support, efficient scans | Data lakes, lakehouses, analytics |

The trade-off for columnar formats is write and update cost: changing one record requires rewriting the column chunks that contain it, which is why Parquet files are treated as **immutable** and why the table formats covered later in this module exist.

### Lab 1.1: CSV versus Parquet on real data

1. Download `yellow_tripdata_2024-01.parquet` from the TLC Trip Record Data page and open DuckDB in the same folder.
2. Inspect the file's structure:

```sql
SELECT * FROM parquet_schema('yellow_tripdata_2024-01.parquet');
SELECT row_group_id, path_in_schema, compression, stats_min, stats_max,
       total_compressed_size, total_uncompressed_size
FROM parquet_metadata('yellow_tripdata_2024-01.parquet')
WHERE path_in_schema IN ('fare_amount', 'payment_type', 'tpep_pickup_datetime');
```

3. Export the same data to CSV and record both file sizes:

```sql
COPY (SELECT * FROM 'yellow_tripdata_2024-01.parquet') TO 'trips.csv' (HEADER);
```

4. Turn on timing with `.timer on`, then run the monthly average fare query above against `'trips.csv'` and against `'yellow_tripdata_2024-01.parquet'`. Run each three times and record the median time.
5. Run `EXPLAIN ANALYZE` on the Parquet query and identify which columns were read.

**Submit:** a short report with a table of file sizes and median query times, the compression ratio you calculated for `payment_type` and for `fare_amount` from the metadata, and a paragraph explaining why the two columns compress so differently.

### Analysis questions

1. A table holds five years of sensor readings, and nearly every query filters on a time range. How would you sort and size the Parquet files to make predicate pushdown effective? What would happen to pushdown if the data were written in random order?
2. A mobile app writes individual user events thousands of times per second. Argue for or against writing those events directly to Parquet, and propose an alternative design.
3. Using the metadata from Lab 1.1, explain why dictionary encoding is effective for `payment_type` but not for `fare_amount`.

### Key terms

Projection pushdown, predicate pushdown, row group, column chunk, page, footer statistics, dictionary encoding, run-length encoding, compression codec, physical versus logical type, immutable file.
