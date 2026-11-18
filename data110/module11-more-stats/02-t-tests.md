# Part 2 - Comparing Means with t-Tests

### Purpose

"Is the average different?" is one of the most common questions an analyst answers: Do manual cars get better mileage than automatics? Did average sales rise after the redesign? Do online students score differently from in-person students? The t-test is the standard tool for answering it.

**After this page, you will be able to:** choose the right type of t-test, check its conditions, run it in R or Excel, and interpret the result.

**Reading:** *OpenIntro Statistics*, Sections 7.1, 7.2, and 7.3.

### Why "t" and not "z"?

In Module 5, you used z-scores with the normal distribution. When we estimate a mean from a sample, we also have to estimate the standard deviation from that same sample, which adds uncertainty. The **t-distribution** accounts for this: it looks like the normal curve but has thicker tails, especially for small samples. As the sample size grows, the t-distribution becomes nearly identical to the normal distribution.

### Three types of t-tests

| Test | Question | Example |
| --- | --- | --- |
| **One-sample** | Is the mean different from a known or target value? | Is the average delivery time different from the promised 30 minutes? |
| **Two-sample (independent)** | Are the means of two separate groups different? | Do manual and automatic cars differ in average mpg? |
| **Paired** | Is the average *change* within the same subjects different from zero? | Did each student's score change from the pre-test to the post-test? |

The most common mistake is using a two-sample test on paired data. If the same people, stores, or products are measured twice, the data are **paired**.

### Conditions

- **Independence:** observations do not influence each other, ideally from a random sample or random assignment.
- **Normality:** the data, or the differences for a paired test, are roughly normal. This matters most for small samples. With 30 or more observations per group and no extreme outliers, the test is reliable even if the data are somewhat skewed, thanks to the Central Limit Theorem from Module 5.

### Worked example: two-sample t-test in R

The built-in `mtcars` dataset includes fuel economy (`mpg`) and transmission type (`am`: 0 = automatic, 1 = manual) for 32 cars.

- **H0:** mean mpg is the same for automatic and manual cars.
- **HA:** mean mpg differs between the two groups.

```r
t.test(mpg ~ am, data = mtcars)

	Welch Two Sample t-test

data:  mpg by am
t = -3.7671, df = 18.332, p-value = 0.001374
alternative hypothesis: true difference in means between group 0 and group 1 is not equal to 0
95 percent confidence interval:
 -11.280194  -3.209684
sample estimates:
mean in group 0 mean in group 1
       17.14737        24.39231
```

**How to read it:**

- The sample means are 17.1 mpg (automatic) and 24.4 mpg (manual).
- The p-value, 0.0014, is far below 0.05, so we **reject H0**: the difference is statistically significant.
- The 95% confidence interval for the difference (automatic minus manual) is about -11.3 to -3.2 mpg. It does not include 0, which agrees with the test, and it tells us manual cars in this data average roughly 3 to 11 more mpg.
- R uses the **Welch** version by default, which does not assume the two groups have equal variances. It is the safer choice.

**Interpretation caution:** this is observational data from 1974 cars. Manual cars in the sample also tend to be lighter, so we cannot conclude the transmission *causes* better mileage. Part 4 returns to this idea.

### Worked example: paired t-test in R

The built-in `sleep` dataset records the extra hours of sleep for the same 10 patients on two different drugs.

```r
drug1 <- sleep$extra[sleep$group == 1]
drug2 <- sleep$extra[sleep$group == 2]
t.test(drug2, drug1, paired = TRUE)

	Paired t-test

data:  drug2 and drug1
t = 4.0621, df = 9, p-value = 0.002833
alternative hypothesis: true mean difference is not equal to 0
95 percent confidence interval:
 0.7001142 2.4598858
sample estimates:
mean difference
           1.58
```

Each patient gained on average 1.58 more hours with drug 2 than with drug 1, and p = 0.0028 indicates the difference is statistically significant. Running this as an unpaired two-sample test would ignore the fact that each patient is compared with themselves and would give a much weaker result.

### Doing it in Excel

Excel's `T.TEST(array1, array2, tails, type)` returns the p-value directly:

| Argument | Values |
| --- | --- |
| tails | 1 = one-sided, 2 = two-sided |
| type | 1 = paired, 2 = two-sample equal variance, 3 = two-sample unequal variance (Welch) |

For example, `=T.TEST(B2:B20, C2:C14, 2, 3)` runs a two-sided Welch test. The **Analysis ToolPak** add-in (File, Options, Add-ins) produces a full output table including means, the t statistic, and p-values.

### Check your understanding

1. A retailer measures daily sales at 12 stores in the month before and the month after a new layout. Which t-test should be used? Why?
2. A t-test comparing two groups returns p = 0.21. Write the conclusion in one sentence for a manager.
3. In the mtcars example, the confidence interval does not include 0. Explain why that matches the small p-value.
4. Why should the mtcars result not be used to claim that switching a car to a manual transmission will improve its mileage?
