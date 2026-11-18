# Part 4 - Correlation and Choosing the Right Test

### Purpose

The hardest part of statistics in practice is often not running a test but **choosing the right one** and explaining what it does and does not show. This page connects correlation to the regression work you did in Module 6, then gives you a decision guide for the tests in this module.

**After this page, you will be able to:** test whether a correlation is significant, explain why correlation does not establish causation, and choose an appropriate test for a given question.

**Reading:** *OpenIntro Statistics*, Section 8.1, "Fitting a line, residuals, and correlation."

### Correlation

**Pearson's correlation coefficient (r)** measures the strength and direction of a **linear** relationship between two numerical variables. It ranges from -1 to 1:

| r | Interpretation |
| --- | --- |
| Close to 1 | Strong positive linear relationship |
| Close to -1 | Strong negative linear relationship |
| Close to 0 | Little or no *linear* relationship (there may still be a curved one) |

Squaring r gives **R-squared**, the proportion of variation in one variable explained by its linear relationship with the other. You saw R-squared in the regression output in Module 6.

### Worked example: is the correlation significant?

```r
cor.test(mtcars$wt, mtcars$mpg)

	Pearson's product-moment correlation

data:  mtcars$wt and mtcars$mpg
t = -9.559, df = 30, p-value = 1.294e-10
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 -0.9338264 -0.7440872
sample estimates:
       cor
-0.8676594
```

- **H0:** the true correlation between weight and mpg is 0. **HA:** it is not 0.
- r = -0.87 shows a strong negative relationship: heavier cars get fewer miles per gallon.
- R-squared = (-0.87)^2 = 0.75, so about 75% of the variation in mpg is explained by weight.
- The p-value is tiny, so the correlation is statistically significant.

In Excel, `=CORREL(range1, range2)` returns r, and `=RSQ(range1, range2)` returns R-squared.

### Correlation is not causation

A strong, significant correlation does not show that one variable causes the other. Three common explanations for a correlation without causation:

- **Confounding variable:** a third variable drives both. In Part 2, manual cars had higher mpg, but they were also lighter. Weight may explain much of the difference that appeared to be about transmission.
- **Reverse causation:** the effect runs the other way. Cities with more police officers may have more crime because more officers are assigned where crime is high.
- **Coincidence:** with enough variables, some will correlate by chance alone.

Causal conclusions require a **randomized experiment** (*OpenIntro* Section 1.4) or careful methods that control for confounders.

### Statistical significance versus practical importance

A p-value tells you whether an effect is likely real, not whether it matters. Always report:

- the **size** of the effect (a difference in means, a difference in proportions, or r), ideally with a **confidence interval**; and
- whether that size is meaningful for the decision at hand.

A significant $0.02 difference in average order value is real but unlikely to justify a business change.

### A caution about running many tests

At alpha = 0.05, about 1 in 20 tests of true null hypotheses will be significant by chance alone. If you test 40 product categories for a difference, expect about 2 "significant" results even if nothing is going on. Decide on your main questions **before** analyzing the data, and be skeptical of a single significant result among many tests.

### Choosing the right test

| Your question | Data | Test | R | Excel |
| --- | --- | --- | --- | --- |
| Is a mean different from a target value? | One numerical variable | One-sample t-test | `t.test(x, mu = 30)` | Analysis ToolPak, or calculate with `T.DIST.2T` |
| Do two separate groups have different means? | Numerical outcome, two groups | Two-sample t-test | `t.test(y ~ group)` | `T.TEST(..., 2, 3)` |
| Did the same subjects change? | Two measurements per subject | Paired t-test | `t.test(after, before, paired = TRUE)` | `T.TEST(..., 2, 1)` |
| Do three or more groups have different means? | Numerical outcome, 3+ groups | ANOVA (*OpenIntro* 7.5) | `aov(y ~ group)` | Analysis ToolPak: ANOVA |
| Does one categorical variable match an expected distribution? | One categorical variable | Chi-square goodness of fit | `chisq.test(counts, p = probs)` | `CHISQ.TEST` |
| Are two categorical variables related? | Two categorical variables | Chi-square test of independence | `chisq.test(table)` | `CHISQ.TEST` |
| Are two numerical variables linearly related? | Two numerical variables | Correlation test | `cor.test(x, y)` | `CORREL`, `RSQ` |
| Can one variable predict another? | Numerical outcome, one or more predictors | Regression (Module 6) | `lm(y ~ x)` | Analysis ToolPak: Regression |

### Check your understanding

1. Choose a test for each question and explain your choice: (a) Is average customer wait time different on weekends than weekdays? (b) Is the proportion of customers choosing each of four menu items equal? (c) Did employees' productivity scores change after a training program? (d) Is advertising spend related to monthly revenue?
2. A study finds that students who use the library more have higher GPAs (r = 0.45, p < 0.001). Give two explanations other than "using the library raises GPA."
3. A test of 20 different website colors finds that one color has a significantly higher click rate (p = 0.04). How much should you trust this result? Why?
