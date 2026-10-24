# Pipeline Orchestration and Scheduling (Concepts)

A real pipeline has many steps that must run in the right order, at the right time, and recover when something fails. **Orchestration** is the coordination of those steps. Tools such as Apache Airflow, Dagster, Prefect, and the schedulers built into cloud platforms all do this job.

### Pipelines as a DAG

Orchestrators represent a pipeline as a **DAG**, a *directed acyclic graph*:

- **Directed:** each step points to the steps that depend on it.
- **Acyclic:** there are no loops; a step never depends on itself.

```
extract_census --\
                  --> load_bronze --> build_silver --> run_tests --> build_gold --> refresh_dashboard
extract_states --/
```

A step runs only after everything it depends on has succeeded. Independent steps, such as the two extracts above, can run at the same time.

### Scheduling and triggers

Pipelines start in one of several ways:

| Trigger | Example |
| --- | --- |
| **Time-based schedule** | Every night at 2:00 AM |
| **Event-based** | When a new file arrives in object storage |
| **Dependency-based** | When an upstream pipeline finishes |
| **Manual** | An engineer reruns a step after a fix |

### Handling failure

Good orchestration plans for things going wrong:

- **Retries:** automatically try a failed step again, since many failures are temporary, such as a network timeout.
- **Alerts:** notify the team by email or chat when a step fails.
- **Stop downstream steps:** if tests fail, do not refresh the dashboard with bad data.
- **Idempotency:** design each step so running it twice gives the same result as running it once, which makes reruns safe.
- **Backfills:** rerun the pipeline for past dates, for example after fixing a bug.

### Monitoring

Orchestrators keep a history of every run: when it started, how long each step took, and what failed. That history helps teams spot slowdowns and prove when data was last refreshed.

### Check yourself

1. Why can't a pipeline's DAG contain a loop?
2. Which steps in the example above could run at the same time?
3. Explain why idempotent steps make it safe to retry after a failure.
