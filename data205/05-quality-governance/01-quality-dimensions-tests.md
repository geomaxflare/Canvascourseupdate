# Dimensions of Data Quality; Automated Data Tests

"Good data" is too vague to manage. Breaking quality into **dimensions** lets us measure it and write tests for it.

### Dimensions of data quality

| Dimension | Question it asks | Example check |
| --- | --- | --- |
| **Accuracy** | Does the data match reality? | County populations match the official census source. |
| **Completeness** | Is anything missing? | No row has an empty `state_code`. |
| **Consistency** | Does it agree with itself and other systems? | The same state is always "OH," never "OHIO" or "Ohio." |
| **Validity** | Does it follow the rules and formats? | `state_abbr` is exactly two letters; dates are real dates. |
| **Uniqueness** | Is anything duplicated? | Each `unique_county_code` appears once. |
| **Timeliness** | Is it fresh enough? | Yesterday's sales are loaded by 6:00 AM. |

### Automated data tests

An **automated data test** checks a rule every time the pipeline runs, instead of relying on someone to notice a problem in a dashboard. Most tests are queries that return the rows breaking a rule. Zero rows means the test passes.

```sql
-- Validity: state abbreviations must be two letters
SELECT state_abbr, COUNT(*) AS bad_rows
FROM silver_county
WHERE LENGTH(state_abbr) <> 2
GROUP BY state_abbr;

-- Timeliness: fail if no data loaded in the last 24 hours
SELECT MAX(loaded_at) AS last_load
FROM bronze_census
HAVING MAX(loaded_at) < NOW() - INTERVAL 1 DAY;
```

### Where tests belong

- **At ingestion (bronze):** check that files arrived, row counts are reasonable, and the expected columns are present.
- **After cleaning (silver):** check uniqueness, validity, and consistency.
- **Before publishing (gold):** check business rules, such as totals reconciling with the source system.

### Severity

Not every failure should stop everything. Teams often label tests as **error**, which stops the pipeline and alerts the owner, or **warning**, which logs the issue and lets the data flow while someone investigates.

### Profiling and monitoring

Besides fixed rules, teams **profile** data to learn its normal patterns, such as typical row counts, null rates, and value ranges, then **monitor** for unusual changes. A sudden 40% drop in daily rows may not break any rule, but it is worth an alert.

### Check yourself

1. Which dimensions were affected by the duplicate Hocking County record and the "OHIO" values in DATA 110?
2. Write a test that finds rows where `population` is null.
3. Which test failures should stop a pipeline, and which should only warn?
