# Part 4 - Verifying AI Output

### Purpose

AI output can look polished and still be wrong, and the errors that matter most in analytics are subtle: a join that silently drops records, a test that does not fit the data, or a number that was never calculated. **Discernment** is the habit of checking AI work the way a careful reviewer would check a colleague's.

**After this page, you will be able to:** recognize common AI errors in analytics work, verify code and results with concrete checks, and decide when an answer is trustworthy enough to use.

### Three things to evaluate

| Evaluate | Question | How to check |
| --- | --- | --- |
| **The product** | Is the output correct and complete? | Run the code, compare with known values, check totals and row counts |
| **The process** | Is the reasoning sound? | Ask the AI to explain its steps and assumptions; check that the method fits the data |
| **The performance** | Did the AI behave as needed? | Did it follow your constraints, admit uncertainty, and stay on the task? |

### Worked example 1: a join that silently drops a state

In the SQL querying lesson, you joined census population to a table of state abbreviations. Suppose you ask an AI:

```
Write a MySQL query that creates a table pop_with_state_abbr with total population
by state_code and state_abbr, joining census_data_by_county_wrangled to state_abbreviations
on state_code.
```

A typical response uses an **inner join**:

```sql
create table pop_with_state_abbr as
select a.state_code, b.state_abbr, sum(population) as total_pop
from census_data_by_county_wrangled a
    join state_abbreviations b on a.state_code = b.state_code
group by 1, 2;
```

The query runs without errors, which is exactly why this mistake is dangerous. A **validation check** reveals the problem: counting distinct state codes in the new table returns 51, while the original has 52. Puerto Rico (state code 72) has no match in the abbreviations table, so the inner join dropped it. Changing to a `left join` keeps all 52.

**Lesson:** "it ran" is not verification. Always compare row counts or totals before and after a transformation, exactly as you did in that lesson.

### Worked example 2: the wrong test for the data

You describe the `sleep` dataset to an AI ("extra hours of sleep for patients on two drugs") without saying the same 10 patients took both drugs. It may suggest a two-sample t-test. Because each patient was measured twice, the correct test is a **paired** t-test (Module 11), which gives a much stronger result (p = 0.003 instead of p = 0.08). The AI did not make an arithmetic mistake; it answered the question as described. Incomplete **Description** led to a wrong **Product**, and only your knowledge of the data could catch it.

### Worked example 3: a number that was never calculated

Ask an assistant without a data analysis tool, "What is the average fare of NYC yellow taxi trips in January 2024?" It may give a confident, specific number. Unless it actually loaded the data and calculated the value, treat that number as unverified. Either compute it yourself or ask the AI to write code you can run on the real file.

### A verification checklist for analytics

- **Run it:** execute every query, formula, or script yourself before using its results.
- **Reconcile:** compare row counts, totals, and minimum and maximum values before and after each step.
- **Spot-check:** look up a few individual records you know, such as Hocking County or Franklin County.
- **Check the method:** does the test or model fit the data type and the question (Module 11's decision table)?
- **Check the source:** for facts or citations, confirm them in an original source; AI-invented citations are common.
- **Ask for reasoning:** "Explain each step and any assumptions you made" often reveals errors.
- **Get a second opinion:** ask the AI to review its own answer as a skeptical reviewer, or compare two tools. Neither replaces your own check.

### Practice (about 30 minutes)

1. Ask an AI to write the inner-join query above (or use the version shown). Run the distinct-count validation from the SQL lesson. Did it catch the missing state?
2. Describe the `sleep` dataset to an AI *without* saying the measurements are paired, and ask which test to use. Then add that detail. Compare the two answers.
3. Ask an AI a factual question about your field and ask it for sources. Check whether the sources exist and say what it claims.

### Check your understanding

1. Why is a query that runs without errors not necessarily correct? Give an example from this course.
2. An AI gives you R output that includes a p-value, but you did not run any code. How should you treat that p-value?
3. Name two checks you would run on an AI-cleaned dataset before using it in a dashboard.
