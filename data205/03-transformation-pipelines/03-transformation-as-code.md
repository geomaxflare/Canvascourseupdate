# Transformation as Code: Version Control, Testing, Documentation

When transformations power reports that leaders rely on, they deserve the same care as software. **Transformation as code** means managing SQL transformations with the practices software teams use. Tools such as **dbt** (data build tool) are built around this idea.

### Version control

Store every transformation as a text file in a **version control** system such as Git.

- Every change is recorded: what changed, who changed it, when, and why.
- Mistakes can be undone by returning to an earlier version.
- Changes are reviewed by a teammate (a *pull request*) before they affect production reports.
- Several people can work on the same project without overwriting each other.

### Automated testing

**Data tests** check that a transformation's output meets expectations every time it runs:

| Test | Example rule |
| --- | --- |
| Not null | `customer_key` is never empty |
| Unique | `unique_county_code` appears only once |
| Accepted values | `state_abbr` is a valid two-letter code |
| Relationships | Every `product_key` in the fact table exists in `dim_product` |
| Custom rule | `population` is greater than 0 |

A data test is usually a query that returns the rows that **break** the rule. Zero rows means the test passes:

```sql
-- Test: unique_county_code must be unique
SELECT unique_county_code, COUNT(*)
FROM silver_county
GROUP BY unique_county_code
HAVING COUNT(*) > 1;
```

If a test fails, the pipeline stops before bad data reaches a dashboard.

### Documentation

Each model should document what it contains, its grain, where its data comes from, and what each column means. Many tools generate a browsable documentation site, including a **lineage graph** showing how models depend on each other, straight from the code and its descriptions.

### Environments

Teams build and test changes in a **development** environment before promoting them to **production**, so experiments never break the reports people use.

### Check yourself

1. How would version control have helped if a cleaning rule from last month introduced an error?
2. Write a test query that finds rows where `population` is missing or negative.
3. Why is it better for a test to stop the pipeline than to let bad data through?
