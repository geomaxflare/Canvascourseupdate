# Assignment - Hypothesis Testing in R

### Purpose

Analysts are often asked whether a difference or relationship in data is real or just random variation. In this assignment, you will run the three tests from this module on real datasets and then explain your findings to someone without a statistics background, which is how this work is used in practice.

**Skills you will practice:**

- Writing null and alternative hypotheses for a question.
- Running a t-test, a chi-square test, and a correlation test in R.
- Interpreting p-values and confidence intervals at a 0.05 significance level.
- Communicating statistical findings, including their limitations, in plain language.

**Knowledge you will gain:** how to choose the right test for a question, and why "statistically significant" does not automatically mean "important" or "causal." These skills appear on the CompTIA Data+ exam and in the Final Exam.

### Task

All three datasets are built into R, so there is nothing to download. Use the module pages as your guide.

**Part A: Two-sample t-test (ToothGrowth).** The `ToothGrowth` dataset records tooth length (`len`) in guinea pigs given vitamin C either as orange juice or as a supplement (`supp`: OJ or VC).

1. Write H0 and HA for the question: "Does average tooth length differ between the two supplement types?"
2. Run `t.test(len ~ supp, data = ToothGrowth)`.
3. Report the two group means, the p-value, and the 95% confidence interval.
4. State your decision at alpha = 0.05 and interpret it in one or two sentences in the context of the question.

**Part B: Chi-square test of independence (HairEyeColor).** The `HairEyeColor` table records hair and eye color for 592 students.

5. Combine the male and female tables with `hair_eye <- apply(HairEyeColor, c(1, 2), sum)` and print the result.
6. Write H0 and HA for the question: "Is hair color related to eye color?"
7. Run `chisq.test(hair_eye)` and check that every expected count is at least 5 using `chisq.test(hair_eye)$expected`.
8. State your decision at alpha = 0.05, and describe one specific pattern in the table that supports your conclusion (for example, compare the eye color of two hair color groups).

**Part C: Correlation (airquality).** The `airquality` dataset records daily ozone levels (`Ozone`) and temperature (`Temp`) in New York in 1973.

9. Create a scatter plot with `plot(airquality$Temp, airquality$Ozone)`.
10. Run `cor.test(airquality$Temp, airquality$Ozone)`. Report r, R-squared, and the p-value.
11. Interpret the strength and direction of the relationship, and explain whether this result shows that higher temperatures *cause* higher ozone levels.

**Part D: Summary for a manager.**

12. Write a summary of 150 to 250 words of your three findings for a manager who has not taken a statistics course. Avoid unexplained technical terms, state what each result means in practical terms, and include at least one limitation of the analysis.

**What to submit:** one Word or PDF document containing your hypotheses, the R output for each test (copied text or screenshots), your answers to each step, and your Part D summary. Also upload your R script (`.R` file).

### Criteria for Success

Your work is graded on the following criteria (3 points total).

| Criterion | Full credit (0.75) | Partial credit (0.4) | No credit (0) |
| --- | --- | --- | --- |
| **Part A: t-test** | Correct H0 and HA; means, p-value, and confidence interval reported; correct decision; interpretation in context | Test run, but hypotheses, decision, or interpretation incomplete or incorrect | Missing |
| **Part B: chi-square** | Correct H0 and HA; expected counts checked; correct decision; a specific pattern from the table described | Test run, but expected counts not checked, or decision or pattern missing | Missing |
| **Part C: correlation** | Scatter plot; r, R-squared, and p-value reported; strength and direction interpreted; correctly explains that correlation does not show causation | Some values or the causation discussion missing or incorrect | Missing |
| **Part D: summary** | 150 to 250 words; plain language; accurate; all three findings; at least one limitation | Missing a finding or the limitation, uses unexplained jargon, or outside the length range | Missing |

**Before you submit, check that you:**

- wrote H0 and HA in words for Parts A and B;
- stated "reject H0" or "fail to reject H0" and explained what that means for the question;
- included the R output for every test;
- explained what the results mean, not only the numbers.

### Example of a strong interpretation

This example uses a different dataset so you can see the expected level of detail:

*"We tested whether manual and automatic cars differ in average fuel economy. Manual cars averaged 24.4 mpg and automatic cars 17.1 mpg. The p-value of 0.001 is below 0.05, so we reject the null hypothesis: the difference is statistically significant. We are 95% confident manual cars average between 3.2 and 11.3 more mpg. Because this is observational data and manual cars in the sample were also lighter, we cannot conclude that the transmission itself causes the higher mileage."*
