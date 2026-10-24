# Module 1: Storage Layers and File Formats

## Introduction

Before we can model, transform, or analyze data, we have to decide how and where it is stored. Those choices quietly decide how fast queries run, how much storage costs, and how easy it is to trust the data later.

In this module, we look at the layers of a modern analytics platform: the file formats data is written in, the low-cost object storage that holds it, the table formats that make those files behave like database tables, and the medallion architecture that organizes data from raw to ready-to-use.

## Objectives

- Compare row-oriented and columnar storage and explain why columnar formats such as Parquet suit analytics.
- Describe object storage and explain how a data lake differs from a traditional database.
- Explain what open table formats such as Delta Lake and Apache Iceberg add on top of plain files.
- Describe the bronze, silver, and gold layers of the medallion architecture and what belongs in each.
