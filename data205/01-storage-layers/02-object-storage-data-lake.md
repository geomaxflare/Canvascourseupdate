# Object Storage and the Data Lake

### Learning outcomes

After this page, you should be able to:

- Describe the data model and guarantees of cloud object storage and contrast them with a file system and a database.
- Explain how separating storage from compute changes the cost and architecture of analytics platforms.
- Design a partitioned folder layout for a data lake and explain how engines use it to prune data.
- Identify the technical and organizational failures that turn a data lake into a "data swamp."

### Required reading

Reis and Housley, *Fundamentals of Data Engineering*, Chapter 6, "Storage," sections on object storage and data lakes, and Chapter 3, "Designing Good Data Architecture," sections comparing the data warehouse, data lake, and data lakehouse.

### The object storage model

Cloud object stores such as Amazon S3, Azure Blob Storage (with Data Lake Storage), and Google Cloud Storage hold data as **objects**. Each object is a blob of bytes, a small set of metadata, and a **key**, stored in a container called a **bucket**:

```
s3://northcoast-analytics/raw/tlc/yellow/year=2024/month=01/yellow_tripdata_2024-01.parquet
```

Although the key looks like a file path, the namespace is **flat**: the slashes are just characters in the key, and "folders" are a convention built on key prefixes. This model has several consequences that every data engineer must design around:

| Property | What it means | Consequence for analytics |
| --- | --- | --- |
| **Whole-object writes** | An object is written in full; it cannot be modified in place or appended to | Tables are built from many immutable files; an update means writing new files |
| **No atomic rename** | Renaming a "folder" means copying and deleting every object under the prefix | The common trick of writing to a temporary folder and renaming it is neither fast nor atomic |
| **Listing is a paginated API call** | Listing a prefix returns keys in batches (1,000 per request on S3) | Discovering the files of a large table by listing can take seconds or minutes |
| **Per-request cost and latency** | Each GET, PUT, and LIST is billed and has tens of milliseconds of latency | Thousands of tiny files are slow and expensive to read |
| **Very high durability and scale** | Data is replicated across devices and facilities; Amazon designs S3 for 99.999999999% durability | Storage is effectively unlimited and rarely lost |
| **Consistency** | Major providers now offer strong read-after-write consistency for individual objects | A newly written object is immediately visible, but a multi-file change is still not atomic as a whole |

That last row is the crux: object storage guarantees correctness one object at a time, while a table is made of many objects. Bridging that gap is the job of the table formats covered on the next page.

### Separating storage from compute

Traditional databases bundle storage and compute on the same servers, so adding storage means paying for compute and vice versa. Object storage **decouples** them:

- Storage is priced per gigabyte-month at a fraction of the cost of database storage, with colder **storage tiers** that are cheaper still for rarely read data.
- Compute (Spark clusters, SQL warehouses, DuckDB on a laptop) is started only when needed and sized to the job.
- Many engines can read the same files, so a data scientist's notebook and a BI warehouse can share one copy of the data instead of maintaining exports.

The trade-off is that every query now reads over the network, which makes file format, file size, and partitioning far more important than on a local disk.

### The data lake

A **data lake** is a centralized repository of data stored in object storage in open formats, holding structured, semi-structured (JSON, logs), and unstructured (documents, images, audio) data. Lakes apply **schema on read**: data is stored as received, and structure is imposed when it is queried. Warehouses traditionally apply **schema on write**: data must conform to a defined table before it is loaded.

| | Data warehouse | Data lake |
| --- | --- | --- |
| Schema | On write | On read |
| Data types | Structured | Structured, semi-structured, unstructured |
| Storage | Proprietary, coupled to compute | Open formats on object storage |
| Transactions and updates | Built in | Not provided by files alone |
| Primary users | Analysts and BI | Engineers and data scientists, increasingly analysts |

### Partitioned layouts

Lakes organize large datasets with **Hive-style partitioning**, encoding column values in the key prefix:

```
raw/tlc/yellow/year=2024/month=01/part-0000.parquet
raw/tlc/yellow/year=2024/month=02/part-0000.parquet
raw/tlc/yellow/year=2024/month=03/part-0000.parquet
```

A query filtering on `year = 2024 AND month = 2` reads only one prefix. This **partition pruning** happens before any file is opened. Good partition columns are frequently filtered, have a moderate number of distinct values, and divide data fairly evenly. Partitioning on a high-cardinality column such as a customer ID produces millions of tiny files, which defeats the purpose.

To make files queryable by name, lakes rely on a **metastore** or **catalog** (historically the Hive Metastore) that maps a table name to a location, a schema, and its partitions. As you will see on the next page, this catalog-plus-folders design, called a **Hive table**, has serious limitations.

### From data lake to data swamp

Lakes fail less often from technology than from the absence of management. Common causes:

- **No ownership or documentation:** nobody knows what a dataset contains or whether it is current.
- **Silent schema drift:** a source adds, renames, or retypes a column, and readers using schema on read break or, worse, misinterpret data.
- **Partial writes:** a job fails halfway, leaving a mix of old and new files that readers treat as a complete table.
- **Small files and unbounded copies:** storage and listing costs grow while query performance falls.
- **Ungoverned access:** sensitive data is copied into broadly readable locations.

### Lab 1.2: Building and querying a partitioned layout

1. Download the January, February, and March 2024 yellow taxi files into one folder.
2. In DuckDB, rewrite all three months into a Hive-partitioned layout:

```sql
COPY (
  SELECT *, year(tpep_pickup_datetime) AS year, month(tpep_pickup_datetime) AS month
  FROM read_parquet('yellow_tripdata_2024-0*.parquet')
  WHERE tpep_pickup_datetime >= '2024-01-01' AND tpep_pickup_datetime < '2024-04-01'
) TO 'lake/yellow' (FORMAT PARQUET, PARTITION_BY (year, month));
```

3. List the folders and files that were created.
4. Compare the plans and timings of a filtered query with and without partition information:

```sql
EXPLAIN ANALYZE
SELECT COUNT(*), AVG(total_amount)
FROM read_parquet('lake/yellow/*/*/*.parquet', hive_partitioning = true)
WHERE month = 2;
```

5. Note the `WHERE` clause in step 2: the TLC files contain a small number of trips with pickup dates outside the file's month. Count them for each file before filtering.

**Submit:** your folder listing, the timing comparison, the count of out-of-range records per file, and a paragraph explaining what those records suggest about the reliability of source data and where in the pipeline they should be handled.

### Analysis questions

1. A team writes each day's data to a temporary prefix and then "renames" it to the final prefix, assuming the switch is instantaneous. Using the properties of object storage, explain what a reader could observe during the rename.
2. An events table is partitioned by `event_date` and `user_id`. Queries filter on dates and occasionally on a single user. Critique the design and propose a better one.
3. Your college wants to store student essays, course evaluations (free text), and enrollment records for analysis. Make the case for or against a data lake, addressing both the technical benefits and the governance risks.

### Key terms

Object, bucket, key prefix, flat namespace, storage tier, separation of storage and compute, schema on read, schema on write, Hive-style partitioning, partition pruning, metastore, Hive table, schema drift, data swamp.
