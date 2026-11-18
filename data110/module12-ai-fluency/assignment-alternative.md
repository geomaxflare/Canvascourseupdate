# Alternative Assignment - Evaluating AI-Assisted Analysis (No AI Use)

### Who this is for

This assignment is for students who choose not to use AI tools for personal reasons. It meets the same learning objectives and is worth the same points as the main assignment, but you will **not** use any AI tool. Instead, you will evaluate sample AI responses prepared for this assignment, check them against your own work, and correct them.

You do not need to explain your reasons for opting out. Send your instructor a Canvas message saying you will complete the alternative assignment, and your instructor will assign it to you in place of the main assignment.

### Purpose

Even if you never use AI yourself, you will work alongside people who do, and you may be asked to review AI-assisted work. Knowing how to plan, question, and verify AI output protects you and your organization from errors that look convincing.

**Skills you will practice:**

- Deciding which parts of an analytics task are suitable for AI (Delegation).
- Evaluating and improving prompts with the CLEAR framework (Description).
- Verifying AI-generated code and explanations against real results (Discernment).
- Recognizing privacy, bias, and disclosure responsibilities (Diligence).

**Knowledge you will gain:** the same understanding of AI's strengths, limits, and risks as the main assignment, applied to analyses you have already completed in this course.

### Task

**Part 1: Delegation plan.** Choose one analysis from earlier in the course: the SQL census data cleaning, the Module 11 hypothesis tests, or the Module 6 regression.

1. Write 3 to 5 sentences describing which parts of that analysis would be reasonable to delegate to an AI tool, which parts should stay with a person, and why.

**Part 2: Evaluate prompts with CLEAR.** Here are two prompts a student might send to an AI assistant:

- Prompt A: "help me with my regression homework"
- Prompt B: "write sql to find duplicates"

2. For each prompt, explain which letters of CLEAR (Concise, Logical, Explicit, Adaptive, Reflective) it fails, using the CLEAR job aid from Part 3.
3. Rewrite each prompt so it would meet CLEAR. You do not need to send your prompts to any AI tool.

**Part 3: Verify three sample AI responses.** Each response below contains at least one error. For each one, apply the six validation steps from Sinclair's Output Analysis Guide (Part 4): break the response into claims, check each claim against your course materials and your own results, and identify what is accurate, incomplete, or wrong.

*Sample Response 1 (SQL).* A student asked for a query to find duplicate counties in `census_cleaning_integrity_exercise_altered`. The AI replied:

```
Here's a query that finds duplicate counties:

SELECT county, COUNT(*) AS n
FROM census_cleaning_integrity_exercise_altered
GROUP BY county
HAVING COUNT(*) > 1;

Every county name returned is a duplicate record that should be deleted.
```

4. Run this query in MySQL Workbench. Report how many rows it returns and give two examples.
5. Explain why the AI's conclusion is wrong, write a corrected query, run it, and show that it finds the real duplicate (Hocking County, 39-073).

*Sample Response 2 (chi-square).* A student pasted the Titanic chi-square output from Module 11 (X-squared = 190.4, df = 3, p-value < 2.2e-16) and asked for an interpretation. The AI replied:

```
The p-value is essentially 0, which means there is a 0% chance that passenger class
had no effect on survival. This proves that being in a lower class caused passengers
to die. Before using this test, you should confirm that the survival data is normally
distributed, since the chi-square test requires normal data.
```

6. Identify every incorrect or misleading claim in this response, and explain why each is wrong using Module 11.
7. Write a correct two-to-three sentence interpretation for a manager.

*Sample Response 3 (regression).* A student pasted the multiple regression output from Module 6 (odometer estimate -6.779e-02, year estimate 9.985e+02, Multiple R-squared 0.7862) and asked what it means. The AI replied:

```
Each additional mile on the odometer lowers the car's price by about $6.78, and each
newer model year adds about $998. The R-squared of 0.7862 means the model's price
predictions are 78.62% accurate. Since mileage has such a strong effect, rolling back
the odometer on a car would increase its value.
```

8. Identify each error. Show your calculation for the correct effect of mileage, stated per mile and per 10,000 miles.
9. Explain what R-squared actually measures.
10. Explain why the final sentence is both a statistical error and an ethical problem.

**Part 4: Diligence scenarios.**

11. A coworker pasted a spreadsheet of student names, ID numbers, and grades into a free AI chatbot to get help finding errors. Using Sinclair's Privacy Guide, explain what went wrong and what the coworker should have done instead.
12. An AI suggests using "home zip code" to predict which applicants will default on a loan. Answer the four bias analysis questions from Part 5 (Representation, Perspective, Fairness, Impact), and name which of the six types of bias this could introduce.
13. Write the AID statement the student in Sample Response 1 should have included if they had submitted the AI's query in their assignment.

**Part 5: Reflection.**

14. Write 250 to 400 words answering: What kinds of mistakes did these AI responses make? Which would have been hardest to catch if you had not already completed these analyses? What do the samples suggest about how analysts should and should not use AI at work? Use each of the four Ds at least once.

**Part 6: Your own disclosure.**

15. End with one sentence confirming that you completed this assignment without using AI tools.

**What to submit:** one Word or PDF document with your answers to every step, including your query results (copied text or screenshots), and your SQL script.

### Criteria for Success

Your work is graded on the following criteria (3 points total).

| Criterion | Full credit (0.6) | Partial credit (0.3) | No credit (0) |
| --- | --- | --- | --- |
| **Delegation plan** | Clear plan stating what could be delegated, what should stay with a person, and why | Plan present but vague or missing reasons | Missing |
| **Prompt evaluation** | Both prompts evaluated against CLEAR with specific reasons; both rewritten to meet CLEAR | Evaluation or rewrite incomplete for one prompt | Missing |
| **Verification** | All three responses checked; SQL run with results shown; every planted error identified and corrected, with the mileage calculation shown | Some errors missed or corrections not supported with evidence | Missing |
| **Diligence** | Privacy problem and fix explained; all four bias questions answered with a bias type named; complete AID statement | One scenario incomplete | Missing |
| **Reflection and disclosure** | 250 to 400 words; specific examples from the samples; uses all four Ds accurately; no-AI confirmation included | Generic, too short, or missing some of the four Ds | Missing |

**Before you submit, check that you:**

- ran the SQL query from Sample Response 1 yourself and included the results;
- explained *why* each planted error is wrong, not only that it is wrong;
- showed your calculation for the mileage effect;
- included your no-AI confirmation.
