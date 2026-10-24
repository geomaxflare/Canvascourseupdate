# Lineage, Cataloging, and Data Contracts

As platforms grow to hundreds of tables and pipelines, people need to answer three questions: *Where did this data come from? What data do we have? Will the data I depend on stay the way I expect?* Lineage, catalogs, and contracts answer them.

### Lineage

**Data lineage** traces data from its sources, through every transformation, to the reports that use it.

```
registration_db.enrollments -> bronze_enrollments -> silver_enrollments -> fact_enrollment -> Enrollment Dashboard
```

Lineage supports:

- **Root-cause analysis:** when a dashboard number is wrong, trace it back to the step that broke.
- **Impact analysis:** before changing a table, see every downstream report it will affect.
- **Compliance:** show auditors where sensitive data flows.

Transformation tools and orchestrators can capture lineage automatically from the code, which keeps it accurate as pipelines change.

### Data catalogs

A **data catalog** is a searchable inventory of an organization's data, like a library catalog for datasets. For each table it typically shows:

- a description, owner, and steward;
- column definitions and data types;
- quality test results and freshness;
- lineage and popular queries;
- tags for sensitive data, such as personal information.

A catalog turns tribal knowledge ("ask Pat, they know that table") into shared, documented knowledge.

### Data contracts

Pipelines often break because a source system changes without warning: a column is renamed, a data type changes, or a field starts arriving empty. A **data contract** is a formal agreement between a data **producer** (the team that owns the source) and its **consumers** (the teams that rely on it).

A contract typically defines:

| Part | Example |
| --- | --- |
| **Schema** | Columns, names, and data types: `enrollment_id` (string, required) |
| **Quality rules** | `term_code` is never null; one row per student per course |
| **Freshness** | Updated daily by 5:00 AM |
| **Ownership** | Registrar's data team; contact and support hours |
| **Change process** | Breaking changes announced 30 days ahead, with a new version |

Contracts are often written as code and checked automatically, so a change that would break the agreement is caught before it reaches downstream pipelines.

### Check yourself

1. A total on the enrollment dashboard dropped by half overnight. How would lineage help you find the cause?
2. What information would you want in a catalog entry before using a table for the first time?
3. Who are the producer and the consumer in a data contract, and what does each promise?
