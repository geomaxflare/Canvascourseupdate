# Row versus Columnar Storage; Parquet

How a file lays out its bytes decides how quickly we can answer analytical questions. Transaction systems and analytics systems need opposite layouts.

### Row-oriented storage

A **row-oriented** format stores all the values of one record together, then the next record, and so on. CSV files and most transactional databases work this way.

```
1, Ohio, Franklin, 1316756
2, Ohio, Cuyahoga, 1235072
3, Ohio, Hamilton, 817473
```

This layout is ideal when an application reads or writes *one whole record at a time*, such as saving a new order or looking up one customer.

### Columnar storage

A **columnar** format stores all the values of one column together:

```
id:         1, 2, 3
state:      Ohio, Ohio, Ohio
county:     Franklin, Cuyahoga, Hamilton
population: 1316756, 1235072, 817473
```

Analytical queries usually touch *a few columns across many rows*, such as "total population by state." With columnar storage, the query reads only the `state` and `population` columns and skips the rest.

### Why columnar wins for analytics

| Benefit | Why it happens |
| --- | --- |
| Less data read | Queries read only the columns they need. |
| Better compression | Values in one column are similar (all states, all numbers), so they compress well. A column of "Ohio, Ohio, Ohio" can be stored as "Ohio × 3". |
| Faster aggregation | Engines can process a column of numbers in tight batches. |

The trade-off: writing or updating a single record is slower, because its values are spread across many column chunks.

### Parquet

**Apache Parquet** is the most widely used open columnar file format. A Parquet file:

- stores data in **row groups**, and within each row group, one **column chunk** per column;
- keeps **metadata** such as the schema, data types, and minimum and maximum values per chunk, so engines can skip chunks that cannot match a filter;
- is **self-describing**: the schema travels with the file, unlike a CSV, where types must be guessed.

Most analytics tools, including Python's pandas, Spark, Power BI, and cloud data warehouses, can read and write Parquet.

### Check yourself

1. A query asks for the average `population` across 3,000 counties in a table with 40 columns. Roughly what fraction of the data does a columnar engine need to read?
2. Why does a column of state names compress better than a full row of mixed data?
3. Name one situation where a row-oriented format is the better choice.
