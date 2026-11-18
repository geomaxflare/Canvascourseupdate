# Assignment - AI-Assisted Analysis with a Prompt Log

### Prefer not to use AI?

If you choose not to use AI tools for personal reasons, you can complete **Alternative Assignment - Evaluating AI-Assisted Analysis (No AI Use)** instead, which meets the same objectives for the same points. You do not need to explain why. Send your instructor a Canvas message before you begin, and your instructor will assign the alternative to you in place of this assignment.

### Purpose

In the workplace, you will be expected to use AI tools to work faster *and* to stand behind every result you deliver. In this assignment, you will redo an analysis you have already completed in this course, this time with an AI assistant. Because you already know what a correct answer looks like, you can judge exactly where the AI helped, where it went wrong, and how you caught it.

**Skills you will practice:**

- Deciding which parts of a task to delegate to AI (Delegation).
- Writing structured prompts with the CLEAR framework and refining them through iteration (Description).
- Verifying AI-generated code and results (Discernment).
- Protecting data and disclosing AI use with an AID statement (Diligence).

**Knowledge you will gain:** a realistic picture of what current AI assistants can and cannot do for an analyst, and a documented workflow you can reuse on the job and describe in interviews.

### Task

**Choose one analysis** from earlier in the course:

- **Option 1, SQL data cleaning:** find and fix the inconsistent `state_abbr` values and the duplicate county record in the census table (Data Cleanliness and Integrity in SQL).
- **Option 2, Hypothesis testing:** complete Part A (t-test) and Part B (chi-square test) of the Module 11 assignment.
- **Option 3, Regression:** model used car price from mileage and model year and predict the price of a 2015 car with 75,000 miles (Module 6).

**Then complete these steps:**

1. **Plan (Delegation).** Before using AI, write 3 to 5 sentences listing which parts of the task you will delegate to AI, which parts you will do yourself, and why.
2. **Prompt (Description).** Use an approved AI assistant to complete the analysis. Write at least one structured prompt that includes task, context, and format, and check it against the CLEAR job aid (Part 3).
3. **Iterate.** Use at least two follow-up prompts to correct, narrow, or extend the AI's work.
4. **Verify (Discernment).** Run all AI-generated code yourself. Perform at least **two** verification checks from Part 4, such as comparing row counts, spot-checking known records, or checking the test's conditions, and compare the AI's results with your original results from earlier in the course. Apply the six validation steps from Sinclair's Output Analysis Guide to at least one AI explanation.
5. **Protect data (Diligence).** Confirm that you shared only public data or column names, never personal information.
6. **Keep a prompt log.** Record every prompt and summarize each response in a table like this:

| # | Prompt (copied exactly) | Summary of the AI's response | What I did next and why |
| --- | --- | --- | --- |
| 1 | ... | ... | ... |

7. **Reflect.** Write 250 to 400 words answering: Where did AI save you time? What did it get wrong or leave out, and how did you catch it? How did your prompts change the results? Would you trust this tool with this task at work, and under what conditions? Use each of the four Ds at least once in your reflection.
8. **Disclose.** End with an AID statement (tool and date, purpose of use, human oversight), as shown in Part 5.

**What to submit:** one Word or PDF document containing your plan, prompt log, verification checks with evidence (output or screenshots), final results, reflection, and AID statement. Also upload your final SQL or R script.

### Criteria for Success

Your work is graded on the following criteria (3 points total).

| Criterion | Full credit (0.6) | Partial credit (0.3) | No credit (0) |
| --- | --- | --- | --- |
| **Delegation plan** | Clear plan stating what was delegated, what was kept, and why | Plan present but vague or missing reasons | Missing |
| **Prompting and iteration** | At least one structured prompt with task, context, and format that meets the CLEAR checklist, and at least two meaningful follow-ups, all logged | Prompts logged but unstructured, or fewer than two follow-ups | Missing |
| **Verification** | Code run by the student; at least two verification checks shown with evidence; results compared with the earlier assignment | Only one check, or checks described without evidence | Missing |
| **Reflection** | 250 to 400 words; specific examples; uses all four Ds accurately; honest assessment of strengths and weaknesses | Generic, too short, or missing some of the four Ds | Missing |
| **Diligence and disclosure** | No personal or confidential data shared; complete AID statement with tool and date, purpose, and human oversight | AID statement missing a part | Missing statement, or sensitive data shared |

**Before you submit, check that you:**

- copied your prompts exactly, including the ones that did not work well;
- ran every piece of AI-generated code yourself;
- showed evidence for each verification check;
- included your AID statement.

### Example of a strong prompt log entry

| # | Prompt (copied exactly) | Summary of the AI's response | What I did next and why |
| --- | --- | --- | --- |
| 3 | "Your query returned 0 rows, but Hocking County (39-073) appears twice in my table. Check whether you grouped on the right column and fix the query." | It admitted it grouped on `county` plus `Population` and rewrote the query to group on `unique_county_code` only. | I ran the new query, which returned Hocking County with a count of 2, matching my result from the SQL assignment. I kept this version. |

Learning from a prompt that did not work is part of the assignment, so include those prompts too. Your grade does not depend on whether the AI was right; it depends on whether **you** caught and handled its mistakes.
