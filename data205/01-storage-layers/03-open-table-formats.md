# Open Table Formats (Delta Lake, Iceberg)

### Learning outcomes

After this page, you should be able to:

- Explain why a directory of Parquet files (a Hive table) cannot provide transactional guarantees on object storage.
- Describe how Delta Lake's transaction log and Apache Iceberg's metadata tree each implement atomic commits and snapshot isolation.
- Explain copy-on-write and merge-on-read strategies for updates and deletes, and when each is preferable.
- Use time travel, schema evolution, and table maintenance operations, and explain their storage implications.

### Required reading

- Shiran, Hughes, and Merced, *Apache Iceberg: The Definitive Guide*, Chapter 2, "The Architecture of Apache Iceberg."
- Lee, Wentling, Haines, and Babu, *Delta Lake: The Definitive Guide*, the chapter on the Delta transaction protocol and Chapter 5, "Maintaining Your Delta Lake."

### The problem with Hive tables

In a Hive table, the table *is* whatever files are currently in its folders. That definition breaks down in several ways:

- **No atomicity:** a job that writes 200 files and fails after 120 leaves readers seeing a partial table.
- **No isolation:** a reader listing files while a writer is replacing them may see some old files and some new ones.
- **Expensive planning:** to find the files, an engine must list every partition folder, which is slow on object storage.
- **Fragile schema changes:** columns are matched by name or position, so renaming or reordering a column can silently misalign data.
- **Rigid partitioning:** changing a partition scheme requires rewriting the entire table, and users must know the scheme to write efficient filters.

Open table formats solve these problems by making a **metadata layer**, not the folder contents, the authoritative definition of the table.

### Delta Lake: the transaction log

A Delta table keeps a `_delta_log` directory next to its data files. Each commit writes a new, sequentially numbered JSON file (`00000000000000000000.json`, `00000000000000000001.json`, and so on) containing **actions**: files added, files removed, schema and table property changes, and commit information. The current state of the table is the result of replaying these actions in order. Every 10 commits by default, Delta also writes a **checkpoint** in Parquet that summarizes the full state, so readers do not have to replay the entire history.

Commits use **optimistic concurrency control**. A writer reads the latest version, writes its data files, and then attempts to create the next log file. Creating a given log file can succeed only once, so if two writers race for version 42, one succeeds and the other must check whether the winning commit conflicts with its own changes, then retry or fail. Readers always see a complete version, which provides **snapshot isolation**.

### Apache Iceberg: the metadata tree

Iceberg organizes metadata as a tree with a catalog at the root:

| Level | Contents |
| --- | --- |
| **Catalog** | Maps the table name to the location of its current metadata file; the commit is an atomic swap of this pointer |
| **Metadata file** | The table's schema, partition specifications, properties, and list of snapshots |
| **Manifest list** | One per snapshot; lists the manifest files that make up that snapshot, with partition-level statistics |
| **Manifest file** | Lists data files and delete files, with per-file column statistics such as value counts and minimum and maximum values |
| **Data and delete files** | The Parquet (or ORC or Avro) files holding rows, plus files that record deleted rows |

Because manifests carry statistics, query planning uses metadata alone to eliminate files, without listing directories. Iceberg also tracks columns by **field ID** rather than name, so renaming, reordering, or dropping columns is safe, and it supports **hidden partitioning**: a table partitioned by `days(pickup_ts)` lets users simply filter on `pickup_ts`, and the partition scheme can later **evolve** (for example, from daily to hourly) without rewriting existing data.

### Updates and deletes: copy-on-write versus merge-on-read

Parquet files are immutable, so a table format must decide how to change a row.

| Strategy | How an update works | Write cost | Read cost | Best when |
| --- | --- | --- | --- | --- |
| **Copy-on-write** | Rewrite every file containing an affected row | High | Low | Updates are infrequent and reads dominate |
| **Merge-on-read** | Write small delete files (Iceberg) or deletion vectors (Delta) marking removed rows; readers merge them at query time | Low | Higher until compaction | Frequent small updates, such as change data capture or privacy deletions |

Merge-on-read tables need periodic **compaction** to rewrite files and fold in deletes, or read performance degrades.

### Time travel and maintenance

Because old versions are retained, both formats support **time travel**:

```sql
-- Delta Lake (Spark SQL)
SELECT COUNT(*) FROM trips VERSION AS OF 3;
SELECT COUNT(*) FROM trips TIMESTAMP AS OF '2026-11-01';

-- Apache Iceberg (Spark SQL)
SELECT COUNT(*) FROM trips VERSION AS OF 8741522906411395410;  -- a snapshot ID
```

Retaining every version forever would grow storage without bound. Maintenance operations reclaim it: Delta's `VACUUM` deletes files no longer referenced by versions within the retention period (seven days by default), and Iceberg's `expire_snapshots` procedure removes old snapshots and their unreferenced files. Once versions are vacuumed or expired, you can no longer time travel to them. This is a policy decision with governance consequences, for example when deleted personal data must truly be removed.

### Comparing the formats

| | Delta Lake | Apache Iceberg |
| --- | --- | --- |
| Source of truth | Ordered JSON log plus Parquet checkpoints | Metadata file referenced by a catalog |
| Commit mechanism | Atomically creating the next log file | Atomically swapping the catalog pointer |
| Schema evolution | Add, and with column mapping enabled, rename and drop | Add, rename, drop, reorder, and widen types by field ID |
| Partitioning | Explicit partition columns, plus clustering options | Hidden partitioning with partition evolution |
| Row-level changes | Copy-on-write or deletion vectors | Copy-on-write or merge-on-read with delete files |

Both formats are open, widely supported, and converging in features. The combination of object storage, an open table format, and SQL engines is what makes a **lakehouse** possible, which Module 2 develops in detail.

### Lab 1.3: Watching a transaction log

1. In Python, write January's trips to a Delta table, then append February's:

```python
import pyarrow.parquet as pq
from deltalake import DeltaTable, write_deltalake

jan = pq.read_table("yellow_tripdata_2024-01.parquet")
feb = pq.read_table("yellow_tripdata_2024-02.parquet")
write_deltalake("delta/trips", jan)
write_deltalake("delta/trips", feb, mode="append")
```

2. Open the `delta/trips/_delta_log` folder. Read both JSON files and identify the `add` actions, the `metaData` action, and the `commitInfo` action.
3. Overwrite the table with only January's trips that have a positive fare, then inspect the new log file and find the `remove` actions:

```python
import pyarrow.compute as pc
write_deltalake("delta/trips", jan.filter(pc.field("fare_amount") > 0), mode="overwrite")
```

4. Compare row counts across versions:

```python
for v in range(3):
    print(v, DeltaTable("delta/trips", version=v).to_pyarrow_table().num_rows)
print(DeltaTable("delta/trips").history())
```

5. Count the Parquet files in `delta/trips`. Explain why files from version 0 are still present after the overwrite.

**Submit:** the row counts for each version, an annotated excerpt of each log file, and a paragraph explaining what `VACUUM` would delete and what you would lose by running it.

### Analysis questions

1. Two jobs append to the same Delta table at the same moment. Walk through what happens at commit time, and explain why the outcome differs if one job deletes rows that the other is updating.
2. A table receives 50,000 small updates per hour from a change data capture feed and is queried by dashboards every few minutes. Recommend copy-on-write or merge-on-read, and describe the maintenance schedule the table will need.
3. A student requests deletion of their personal data under institutional policy. Explain why deleting the rows is not sufficient on a table format with time travel, and what additional steps are required.

### Key terms

Hive table, metadata layer, transaction log, commit, checkpoint, optimistic concurrency control, snapshot isolation, manifest list, manifest file, field ID, hidden partitioning, partition evolution, copy-on-write, merge-on-read, deletion vector, compaction, time travel, VACUUM, snapshot expiration, lakehouse.
