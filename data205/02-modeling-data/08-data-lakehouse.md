# The Data Lakehouse: Bringing It Together

Module 1 introduced the pieces of a **data lakehouse**: low-cost object storage, open table formats such as Delta Lake and Apache Iceberg, and the medallion layers. This page shows how the modeling ideas from this module are built and maintained on that platform.

### What a lakehouse combines

| From the data lake | From the data warehouse |
| --- | --- |
| Low-cost object storage for any type of data | Reliable tables with ACID transactions |
| Open file formats readable by many tools | Schema enforcement and SQL access |
| Room for raw, unstructured, and machine learning data | Performance and governance for BI reporting |

Instead of copying data from a lake into a separate warehouse, one copy of the data serves both data science and business reporting.

### Where the models live

| Layer | Modeling approach | Example |
| --- | --- | --- |
| **Bronze** | Raw copies of source data | `bronze_registration_enrollments` |
| **Silver** | Cleaned, integrated entities; master data golden records; sometimes Data Vault | `silver_student`, `silver_enrollment` |
| **Gold** | Star schemas, aggregate tables, and wide tables for reporting | `fact_enrollment`, `dim_student`, `dim_course`, `dim_term` |

### Maintaining a Type 2 dimension with MERGE

Open table formats support `MERGE`, which updates, inserts, and expires rows in one atomic step. That makes slowly changing dimensions practical directly on lakehouse tables. A simplified Type 2 update in two steps:

```sql
-- 1. Expire the current row for students whose program changed
MERGE INTO gold.dim_student AS d
USING silver.student AS s
  ON d.student_id = s.student_id AND d.is_current = true
WHEN MATCHED AND d.program <> s.program THEN
  UPDATE SET d.is_current = false, d.valid_to = current_date();

-- 2. Insert a new current row for new students and for students just expired
INSERT INTO gold.dim_student (student_id, name, program, valid_from, valid_to, is_current)
SELECT s.student_id, s.name, s.program, current_date(), DATE '9999-12-31', true
FROM silver.student AS s
LEFT JOIN gold.dim_student AS d
  ON d.student_id = s.student_id AND d.is_current = true
WHERE d.student_id IS NULL;
```

If a load goes wrong, **time travel** lets the team see the dimension as it was before the load and restore it.

### The semantic layer

Even with a clean star schema, two dashboards can calculate "enrollment" differently. A **semantic layer** defines business metrics once, such as the formula for "full-time equivalent enrollment" or "retention rate," along with approved joins and names. BI tools then use those shared definitions instead of each report reinventing them. Power BI semantic models are one example.

### Governance in one place

Because all layers live on one platform, a lakehouse can apply the same **catalog**, **access controls**, **lineage**, and **quality tests** from raw files to finished reports, a theme we return to in the Data Quality and Governance module.

### Check yourself

1. Which layer would hold the golden record for students? Which would hold `fact_enrollment`?
2. In the MERGE example, why is the current row expired instead of simply updated?
3. How does a semantic layer prevent two dashboards from reporting different enrollment numbers?
