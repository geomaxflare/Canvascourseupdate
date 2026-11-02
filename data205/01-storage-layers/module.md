# Module 1: Storage Layers and File Formats

## Introduction

Every analytical query is ultimately a request to read bytes from storage, and on modern platforms reading bytes, not computing, is usually the bottleneck. How data is laid out on disk, where it is stored, and how a set of files is turned into a reliable table determine the cost, speed, and trustworthiness of everything built on top of it.

This module works from the bottom of the stack up: the internal structure of columnar file formats such as Apache Parquet; the semantics and economics of cloud object storage and the data lakes built on it; the metadata layer that open table formats (Delta Lake and Apache Iceberg) add to provide transactions, versioning, and schema evolution; and the medallion architecture used to organize a lakehouse into progressively refined layers. Throughout the module, you will work hands-on with a real dataset: roughly three million New York City taxi trips per month, published as Parquet by the NYC Taxi and Limousine Commission.

## Objectives

- Explain how row-oriented and columnar layouts interact with the access patterns of transactional and analytical workloads, and quantify the difference in data read for a given query.
- Describe the internal structure of a Parquet file, including row groups, column chunks, pages, encodings, and footer statistics, and explain how query engines use that structure for projection and predicate pushdown.
- Analyze the semantics of object storage (immutability, key-based namespaces, listing, consistency) and their consequences for building tables on files.
- Compare how Delta Lake and Apache Iceberg implement atomic commits, snapshot isolation, time travel, and schema and partition evolution.
- Design a bronze, silver, and gold pipeline with explicit quality rules, idempotent loads, and a clear contract for each layer.

## Readings

- Reis and Housley, *Fundamentals of Data Engineering*, Chapter 6, "Storage," and the data lake, data warehouse, and lakehouse sections of Chapter 3, "Designing Good Data Architecture."
- Shiran, Hughes, and Merced, *Apache Iceberg: The Definitive Guide*, Chapter 2, "The Architecture of Apache Iceberg."
- Lee, Wentling, Haines, and Babu, *Delta Lake: The Definitive Guide*, the chapters on the Delta transaction protocol and Chapter 5, "Maintaining Your Delta Lake."
- All three books are available free through the LCCC library's O'Reilly Learning subscription.

## Tools and Data

- **DuckDB** (free, runs on Windows, Mac, and Linux): install the command-line tool or the Python package (`pip install duckdb`).
- **Python 3** with `pandas`, `pyarrow`, and `deltalake` (`pip install pandas pyarrow deltalake`) for the table format lab.
- **NYC TLC Trip Record Data:** download the Yellow Taxi trip records for January through March 2024 and the Taxi Zone Lookup Table from the TLC Trip Record Data page (nyc.gov/site/tlc/about/tlc-trip-record-data.page).
