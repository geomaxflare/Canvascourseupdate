# Provenance and Documentation of Training Data

When a model makes a decision that affects people, someone will eventually ask: *What was it trained on?* **Provenance** is the documented history of a dataset: where it came from, how it was collected, and every change made to it. Without it, no one can explain a model's behavior, fix its problems, or show that it was built responsibly.

### What to record

| Question | Example |
| --- | --- |
| **Source** | Where did the data come from? Which systems, vendors, or websites? |
| **Collection** | How and when was it collected? Who or what was included or left out? |
| **Rights and consent** | Are we allowed to use it for this purpose? Under what license or agreement? |
| **Processing** | What cleaning, filtering, labeling, and de-duplication steps were applied? By which version of the code? |
| **Composition** | How many records? What is the balance across groups, regions, or time periods? |
| **Known limitations** | What gaps or biases are known? Where should the data not be used? |
| **Version** | Which exact snapshot of the dataset trained which model version? |

### Datasheets for datasets

A widely used practice is the **datasheet**: a short, structured document that travels with a dataset, much like the specification sheet for an electronic part. A datasheet answers the questions above in plain language for anyone who might use the data. A similar idea for models, often called a **model card**, documents what a model is for, how it was evaluated, and its limitations.

### Building provenance into the pipeline

Provenance is far easier to capture automatically than to reconstruct later:

- Keep **raw data** in the bronze layer and never edit it in place.
- **Version datasets** with table formats that support time travel, or with snapshot IDs.
- **Version the code** that prepares the data, and record which code version produced which dataset.
- Use **lineage** to link each training set to its sources and each model to its training set.
- Store **datasheets** in the data catalog next to the dataset.

### Why it matters

- **Accountability:** explain and defend a model's decisions.
- **Reproducibility:** rebuild the exact training set to retrain or audit a model.
- **Compliance:** show that personal data was used with permission and handled correctly.
- **Fixing problems:** when bias or errors are found, trace them back to the data that caused them.

### Check yourself

1. A model performs poorly for one region. Which provenance information would help you investigate?
2. Why is it hard to reconstruct provenance after the fact?
3. Draft three questions you would include in a datasheet for the census dataset used in this program.
