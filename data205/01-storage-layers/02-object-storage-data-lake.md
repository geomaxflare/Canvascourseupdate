# Object Storage and the Data Lake

Modern analytics platforms store most of their data as files in low-cost, nearly unlimited **object storage**. Understanding this layer explains why the "data lake" exists and what problems it creates.

### What object storage is

Object storage, such as Amazon S3, Azure Blob Storage, or Google Cloud Storage, keeps data as **objects**: a file, some metadata, and a unique key (a path-like name).

```
s3://lccc-analytics/raw/census/2020/county_population.parquet
```

Key properties:

- **Scales almost without limit** and costs far less per gigabyte than database storage.
- **Separates storage from compute**: many different tools can read the same files, and processing power is paid for only when used.
- **Objects are written whole.** There is no "update row 52"; to change a file, you write a new version of it.

### The data lake

A **data lake** is a central store of an organization's data, kept as files in object storage, in its raw or lightly processed form. It can hold structured data (tables), semi-structured data (JSON, logs), and unstructured data (images, PDFs, audio).

| | Data warehouse | Data lake |
| --- | --- | --- |
| Data shape | Structured tables | Any format |
| Schema | Defined before loading (*schema on write*) | Applied when read (*schema on read*) |
| Storage cost | Higher | Lower |
| Typical users | Analysts, BI reports | Data engineers, data scientists, and analysts |

### The "data swamp" problem

Because anything can be dropped into a lake, lakes often become **data swamps**: thousands of files with no clear owner, no documentation, duplicate copies, and no guarantee of quality. Plain files also lack features analysts expect from databases, such as safe concurrent updates and the ability to roll back a bad load.

The next two topics address these problems: **open table formats** add database features to files, and the **medallion architecture** adds organization.

### Check yourself

1. What does "separating storage from compute" allow an organization to do?
2. Explain the difference between *schema on write* and *schema on read*.
3. Which data governance practices from earlier courses would help prevent a data swamp?
