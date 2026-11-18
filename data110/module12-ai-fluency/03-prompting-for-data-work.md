# Part 3 - Prompting for Data Work

### Purpose

The quality of an AI's answer depends heavily on the quality of the request. This page gives you a structure for writing prompts (the **Description** competency) and shows how to improve results through conversation instead of starting over.

**After this page, you will be able to:** write a structured prompt for an analytics task, use examples and constraints to shape the output, and refine results with iteration and prompt chaining.

### The parts of a strong prompt

| Element | What to include | Example for data work |
| --- | --- | --- |
| **Task** | The specific action you want | "Write a MySQL query that..." |
| **Context** | The data, its structure, and the goal | Table name, column names and types, what one row represents, why you need the result |
| **Role** | A perspective for the AI to take | "Act as a data analyst reviewing my work for errors." |
| **Format** | What the output should look like | "Return only the query, then a one-sentence explanation of each clause." |
| **Constraints** | Limits and requirements | "Use only standard SQL. Do not modify the table." |
| **Examples** | One or more samples of input and desired output | A few rows showing the problem, such as `OHIO` where `OH` belongs |

You do not need every element every time, but **task** and **context** are almost always essential. Never include personal or confidential data in a prompt; use made-up sample rows or column names only (see Part 5).

### Worked example: a weak and a strong prompt

**Weak prompt:**

```
fix my state data
```

The AI has to guess the tool, the table, what "fix" means, and what is wrong. You will get a generic answer.

**Strong prompt:**

```
I'm a data analytics student using MySQL 8. My table census_cleaning_integrity_exercise_altered
has one row per U.S. county with these columns:
Record_No (int), state (text), county (text), unique_county_code (text, like '39-073'),
state_abbr (text, should be a 2-letter code like 'OH'), Population (int).

Some rows have problems:
- state_abbr sometimes contains a full name, such as 'OHIO' or 'MISSISSIPPI'.
- Some counties appear twice with the same unique_county_code.

Write two SELECT queries (do not update or delete anything yet):
1. List every state_abbr value that is not exactly 2 characters, with a count of rows for each.
2. List every unique_county_code that appears more than once, with its count.
After each query, explain in one sentence what it does.
```

This prompt states the tool and version, describes what one row represents, lists exact column names and types, shows the problem with real examples, sets a safety constraint (SELECT only), and specifies the format.

### Checking a prompt with CLEAR

Sinclair College's AI Excellence Institute uses the **CLEAR** framework, developed by librarian Leo Lo and adapted by Sinclair, as a checklist for drafting and evaluating prompts. Download the [CLEAR Prompting Job Aid](https://www.sinclair.edu/sites/www/assets/File/Hom-Aca-AcaDiv-eLearn/PromptingJobAid%28CLEARFramework%29.pdf) and keep it next to you as you work.

| Letter | Goal | Check for the census prompt above |
| --- | --- | --- |
| **C**oncise | A focused prompt with a clear task verb (describe, analyze, write, summarize); no unnecessary words | "Write two SELECT queries" states the task directly |
| **L**ogical | Instructions in a clear, sensible order | Context first, then the problems, then numbered queries |
| **E**xplicit | Output requirements: format, audience, tone, and constraints | SELECT only, MySQL 8, one-sentence explanation after each query |
| **A**daptive | Refine through follow-up prompts when the output misses the goal | The follow-up prompts in the next section |
| **R**eflective | Verify every claim in the output and check sources | Running the queries against the real table (Part 4) |

The prompt elements in the table at the top of this page tell you *what* to include; CLEAR tells you *how well* the prompt is written and reminds you that the work is not finished until the output is verified.

### Iteration: treat it as a conversation

The first answer is a draft. Improve it with follow-up prompts instead of rewriting from scratch:

- **Correct:** "The second query returned 0 rows, but I know Hocking County is duplicated. Check whether you grouped on the right column."
- **Narrow:** "Now show only Ohio rows."
- **Explain:** "Explain why you used HAVING instead of WHERE."
- **Extend:** "Write an UPDATE that changes 'OHIO' to 'OH', and a SELECT I can run afterward to confirm it worked."

### Prompt chaining

For larger tasks, break the work into a sequence of prompts, where each step builds on the last and you check the result before continuing:

1. "Here are the column names and 5 sample rows of `mtcars`. Describe the variables and suggest what questions this data could answer."
2. "For the question 'Do manual and automatic cars differ in average mpg?', which statistical test fits, and what are its conditions?"
3. "Write R code to check the conditions and run that test."
4. "Here is my R output: (paste output). Help me write a two-sentence interpretation for a manager."

Chaining keeps each step small enough to verify, and it keeps *you* in charge of the decisions between steps, which is exactly what the Delegation competency asks.

### Asking AI to improve your prompt

When you are unsure how to ask, ask the AI: "Before you answer, ask me any questions you need to give a good answer." This often surfaces context you forgot to include, such as the database type or the size of the data.

### Practice (about 30 minutes)

Using any approved AI assistant:

1. Send the weak prompt "fix my state data" and save the response.
2. Send the strong prompt above and save the response.
3. Run the queries from the strong prompt in MySQL Workbench against your census table from Module 3. Do they find the problems you found before?
4. Write one follow-up prompt that improves the result, and note what changed.

Check your strong prompt against each letter of CLEAR. Keep your notes; you will use this practice in the assignment.

### Check your understanding

1. Rewrite this prompt to be stronger: "make a chart of the car data."
2. Why does including a few example rows often improve SQL and R code from an AI?
3. What is the difference between iteration and prompt chaining?
