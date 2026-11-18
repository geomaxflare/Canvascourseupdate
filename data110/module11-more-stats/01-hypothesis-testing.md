# Part 1 - Hypothesis Testing and P-Values

### Purpose

Every statistical test in this module follows the same logic. Once you understand that logic, a t-test, a chi-square test, and a regression output all read the same way: state a claim, measure the evidence against it, and decide.

**After this page, you will be able to:** write null and alternative hypotheses, interpret a p-value, and explain Type I and Type II errors.

**Reading:** *OpenIntro Statistics*, Section 5.3, "Hypothesis testing for a proportion."

### The logic of a hypothesis test

A hypothesis test works like a courtroom. The defendant is presumed innocent until the evidence makes that presumption hard to believe.

| Courtroom | Hypothesis test |
| --- | --- |
| Presumed innocent | **Null hypothesis (H0):** there is no effect, no difference, or no relationship |
| The prosecution's claim | **Alternative hypothesis (HA):** there is an effect, a difference, or a relationship |
| Evidence presented | The sample data and a **test statistic** that measures how far the data are from what H0 predicts |
| "Beyond a reasonable doubt" | The **significance level (alpha)**, usually 0.05 |
| Verdict: guilty or not guilty | **Reject H0** or **fail to reject H0** |

Notice the second verdict is "not guilty," not "innocent." In the same way, we never "accept" or "prove" the null hypothesis. We only conclude that the data did not provide strong enough evidence against it.

### Writing hypotheses

A coffee chain claims its new loyalty app increases the average purchase above the current $6.50.

- **H0:** the average purchase with the app is $6.50 (no change).
- **HA:** the average purchase with the app is greater than $6.50.

This is a **one-sided** test, because the claim is about one direction. If the question were "does the app change the average purchase, up or down?", HA would be "not equal to $6.50," a **two-sided** test. Use a two-sided test unless you had a specific direction in mind *before* looking at the data.

### The p-value

The **p-value** is the probability of getting results at least as extreme as the ones observed, *if the null hypothesis were true*.

- A **small p-value** (below alpha, usually 0.05) means the data would be surprising if H0 were true, so we **reject H0**. The result is called **statistically significant**.
- A **large p-value** means the data are consistent with H0, so we **fail to reject H0**.

Common misreadings to avoid:

| Misreading | Correct statement |
| --- | --- |
| "p = 0.03 means a 3% chance the null hypothesis is true." | It means a 3% chance of seeing data this extreme *if* H0 were true. |
| "p = 0.40 proves there is no effect." | It means the data did not give strong evidence of an effect. The sample may be too small to detect one. |
| "Significant means important." | A tiny, unimportant difference can be significant in a very large sample. Always report the size of the effect too. |

### Type I and Type II errors

Because decisions are based on samples, two kinds of mistakes are possible:

| | H0 is actually true | H0 is actually false |
| --- | --- | --- |
| **Reject H0** | **Type I error** (false positive) | Correct decision |
| **Fail to reject H0** | Correct decision | **Type II error** (false negative) |

- The chance of a Type I error equals alpha. Choosing alpha = 0.05 means accepting a 5% risk of declaring an effect that is not real.
- Lowering alpha reduces Type I errors but makes Type II errors more likely. Larger samples reduce Type II errors.
- Which error is worse depends on the situation. Approving an ineffective drug (Type I) may be worse than missing a slightly better marketing email (Type II).

### Connection to confidence intervals

In Module 5, you built confidence intervals. A 95% confidence interval and a two-sided test at alpha = 0.05 always agree: if the null value (for example, $6.50) falls **outside** the 95% interval, the test rejects H0; if it falls **inside**, the test fails to reject H0. Reporting the interval is often more useful than the p-value alone, because it also shows the size of the effect.

### Before you test: how the sample was drawn

A test is only as good as the sample. The CompTIA Data+ objectives expect you to recognize these sampling methods (see also *OpenIntro* Section 1.3):

| Method | How it works | Watch out for |
| --- | --- | --- |
| Simple random | Every member has an equal chance of selection | Needs a complete list of the population |
| Stratified | Divide into groups (strata), randomly sample from each | Ensures small groups are represented |
| Systematic | Select every nth member after a random start | Bias if the list has a repeating pattern |
| Cluster | Randomly select whole groups (such as classrooms) | Clusters may differ from each other |
| Multistage | Combine methods in stages, such as clusters then random | More complex to analyze |
| Convenience | Use whoever is easiest to reach | Usually not representative; avoid for inference |
| Snowball | Participants recruit other participants | Useful for hard-to-reach groups, but biased |

### Check your understanding

1. A school claims its new tutoring program raises the average exam score above 70. Write H0 and HA. Is this one-sided or two-sided?
2. A test returns p = 0.12 with alpha = 0.05. State your decision and write one sentence explaining it to a manager.
3. A bank's fraud model flags a legitimate purchase as fraud. Is this a Type I or Type II error if H0 is "the purchase is legitimate"?
4. A survey of 50,000 customers finds a statistically significant difference of $0.02 in average spending between two regions. Should the company act on it? Why or why not?
