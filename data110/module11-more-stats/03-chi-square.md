# Part 3 - Chi-Square Tests for Categorical Data

### Purpose

t-tests compare averages of numbers. Many business questions are about **categories** instead: Is customer satisfaction (satisfied, neutral, dissatisfied) related to region? Are website visits spread evenly across the days of the week? Chi-square tests answer these questions by comparing the counts you observed with the counts you would expect if nothing interesting were going on.

**After this page, you will be able to:** choose between a goodness of fit test and a test of independence, check the conditions, run each test, and interpret the result.

**Reading:** *OpenIntro Statistics*, Sections 6.3 and 6.4.

### The chi-square statistic

Both chi-square tests use the same idea. For each category or cell:

```
chi-square = sum of (observed - expected)^2 / expected
```

If the observed counts are close to the expected counts, the statistic is small and the p-value is large. The bigger the gaps, the larger the statistic and the smaller the p-value. The **degrees of freedom** depend on the number of categories, and the p-value comes from the chi-square distribution.

**Conditions:** the counts come from independent observations, and every **expected** count is at least 5. When expected counts are smaller, combine categories or use a different method.

### Two chi-square tests

| Test | Variables | Question | Example |
| --- | --- | --- | --- |
| **Goodness of fit** | One categorical variable | Does the distribution match an expected distribution? | Are orders spread evenly across the 7 days of the week? |
| **Test of independence** | Two categorical variables | Are the two variables related? | Is passenger class related to survival on the Titanic? |

### Worked example: goodness of fit

A game company claims its digital die is fair. In 120 rolls, each face should appear 20 times.

| Face | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Observed | 25 | 17 | 15 | 23 | 24 | 16 |
| Expected | 20 | 20 | 20 | 20 | 20 | 20 |

- **H0:** the die is fair (each face has probability 1/6).
- **HA:** the die is not fair.

```
chi-square = (25-20)^2/20 + (17-20)^2/20 + (15-20)^2/20 + (23-20)^2/20 + (24-20)^2/20 + (16-20)^2/20
           = (25 + 9 + 25 + 9 + 16 + 16) / 20 = 5.0     with 6 - 1 = 5 degrees of freedom
```

```r
chisq.test(c(25, 17, 15, 23, 24, 16))

	Chi-squared test for given probabilities

data:  c(25, 17, 15, 23, 24, 16)
X-squared = 5, df = 5, p-value = 0.4159
```

With p = 0.42, we **fail to reject H0**. The variation in the counts is the kind we would expect from a fair die. This does not prove the die is fair; it means the data give no strong evidence that it is not.

### Worked example: test of independence

R's built-in `Titanic` table records the 2,201 people aboard by class and survival. Summing over sex and age gives a two-way table:

| Class | Did not survive | Survived |
| --- | --- | --- |
| 1st | 122 | 203 |
| 2nd | 167 | 118 |
| 3rd | 528 | 178 |
| Crew | 673 | 212 |

- **H0:** survival is independent of class.
- **HA:** survival is related to class.

```r
class_survival <- apply(Titanic, c(1, 4), sum)
chisq.test(class_survival)

	Pearson's Chi-squared test

data:  class_survival
X-squared = 190.4, df = 3, p-value < 2.2e-16
```

The p-value is essentially zero, so we **reject H0**: survival was strongly related to class. The test tells us *that* a relationship exists, not *what* it looks like, so always follow up by comparing proportions: about 62% of first-class passengers survived (203 of 325), compared with about 25% of third-class passengers (178 of 706). The expected counts for each cell are available with `chisq.test(class_survival)$expected`.

The degrees of freedom for a test of independence are (rows - 1) x (columns - 1) = (4 - 1) x (2 - 1) = 3.

### Doing it in Excel

`CHISQ.TEST(actual_range, expected_range)` returns the p-value. For a test of independence, first calculate each expected count as (row total x column total) / grand total, then pass both tables to `CHISQ.TEST`.

### Check your understanding

1. A store wants to know whether its customers' preferred payment method (cash, card, mobile) differs by age group (under 30, 30 to 50, over 50). Which chi-square test applies? Write H0 and HA.
2. A goodness of fit test on 7 days of the week has how many degrees of freedom?
3. One cell in your table has an expected count of 2. What should you do?
4. Using the Titanic table, calculate the survival rate for the crew. How does it compare with first class?
