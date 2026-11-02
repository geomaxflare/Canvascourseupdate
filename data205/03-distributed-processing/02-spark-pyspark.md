# Spark and PySpark Fundamentals

**Apache Spark** is the most widely used open-source engine for distributed data processing. **PySpark** is its Python interface. Spark also supports SQL, so much of what you know already transfers directly.

### How Spark is organized

| Part | Role |
| --- | --- |
| **Driver** | The coordinator. It runs your program, plans the work, and assigns tasks. |
| **Executors** | Worker processes on the cluster's machines that do the actual processing. |
| **Partitions** | Chunks of the data. Each task processes one partition, so many partitions can be processed at once. |

### DataFrames

Spark's main data structure is the **DataFrame**: a table with named columns, spread across the cluster in partitions. It works much like a data frame in R or pandas.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("census").getOrCreate()

counties = spark.read.parquet("s3://lccc-analytics/silver/county/")

state_totals = (
    counties
    .filter(F.col("population") > 0)
    .groupBy("state")
    .agg(F.sum("population").alias("total_pop"))
    .orderBy(F.desc("total_pop"))
)

state_totals.show(10)
state_totals.write.mode("overwrite").parquet("s3://lccc-analytics/gold/state_population/")
```

The same work in Spark SQL:

```python
counties.createOrReplaceTempView("counties")
spark.sql("""
  SELECT state, SUM(population) AS total_pop
  FROM counties WHERE population > 0
  GROUP BY state ORDER BY total_pop DESC
""").show(10)
```

### Lazy evaluation

Spark operations come in two kinds:

- **Transformations** such as `filter`, `select`, `groupBy`, and `join` only *describe* work. Nothing runs yet.
- **Actions** such as `show`, `count`, and `write` *trigger* the work.

Waiting until an action lets Spark see the whole plan and optimize it, for example by reading only the needed columns and filtering before a join.

### Shuffles

Some operations, such as `groupBy` and `join`, need all rows with the same key on the same machine. Spark moves data across the network to arrange this, which is called a **shuffle**. Shuffles are often the slowest part of a job, so reducing them is a key performance skill.

### Check yourself

1. What is the difference between the driver and the executors?
2. In the example, which line actually causes Spark to start processing?
3. Why does a `groupBy` usually require a shuffle?
