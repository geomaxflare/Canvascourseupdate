# Module 4: Distributed Processing

## Introduction

Every tool we have used so far, including Excel, R, and a single MySQL database, runs on one computer. Eventually, data grows too large or arrives too fast for one machine. In this module, we learn when that happens, how distributed engines like Apache Spark split work across many machines, and how the way data is partitioned decides whether a query takes seconds or hours.

## Objectives

- Identify the signs that a workload has outgrown a single machine, and the options to try first.
- Explain how Spark distributes work using a driver, executors, and partitions.
- Write basic PySpark DataFrame code to read, filter, group, and write data.
- Explain how partitioning and file layout affect query performance.
