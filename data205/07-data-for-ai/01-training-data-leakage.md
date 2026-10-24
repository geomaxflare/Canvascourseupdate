# Training Data Hygiene and Leakage

A model can only be as reliable as the data it learns from. **Training data hygiene** is the set of practices that keep training data accurate, representative, and fair. **Leakage** is one of the most common and most misleading problems.

### Hygiene checklist

- **Clean and consistent:** apply the same quality dimensions as any analytics data: no duplicates, valid values, consistent formats.
- **Representative:** the data should reflect the situations where the model will be used. A model trained only on one region may fail in another.
- **Balanced and fair:** check whether some groups are under-represented, and whether the features act as proxies for protected characteristics, as in the recidivism case study from DATA 110.
- **Correctly labeled:** for supervised learning, wrong labels teach the model wrong answers.
- **Privacy-aware:** remove or mask personal information the model does not need.

### Splitting the data

Data is split into separate sets:

| Set | Purpose |
| --- | --- |
| **Training** | The model learns from it. |
| **Validation** | Used to tune and compare models. |
| **Test** | Held back until the end to estimate real-world performance. |

The test set must stay untouched until the final evaluation. If it influences any decision, its score is no longer an honest estimate.

### Data leakage

**Leakage** happens when the model sees information during training that it will not have when making real predictions. The model looks excellent in testing, then fails in use.

| Type | Example |
| --- | --- |
| **Target leakage** | Predicting whether a customer will cancel, using a "cancellation reason" column that is only filled in *after* they cancel. |
| **Time leakage** | Randomly splitting sales data, so the model trains on next month's data to "predict" last month. |
| **Train/test contamination** | The same customer, or duplicate records, appear in both training and test sets. |
| **Preprocessing leakage** | Calculating averages for scaling or filling missing values using the whole dataset, including the test set. |

### Preventing leakage

- Ask of every feature: *Will this value be known at the moment of prediction?*
- For time-based data, split by time: train on the past, test on the future.
- Split by entity (for example, by customer) so the same person is not on both sides.
- Fit cleaning and scaling steps on the training data only, then apply them to the test data.
- Be suspicious of results that look too good to be true.

### Check yourself

1. A model predicting hospital readmission includes "discharge follow-up scheduled." Could this be leakage? What would you ask?
2. Why should sales data be split by date instead of randomly?
3. How could duplicate records cause a model's test score to be too high?
