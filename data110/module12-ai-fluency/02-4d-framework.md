# Part 2 - The 4D AI Fluency Framework

### Purpose

"Be careful with AI" is not a method. The 4D framework turns AI fluency into four competencies you can practice and check, so that every time you use AI you know what to decide, what to write, what to check, and what you are responsible for.

**After this page, you will be able to:** describe the four competencies and the three ways people work with AI, and apply them to an analytics task.

**Source:** Dakan and Feller, *AI Fluency: Framework and Foundations* (Anthropic Academy, CC BY-NC-SA 4.0). Enrolling in this free course is optional but recommended.

### Three ways of working with AI

| Mode | What it means | Analytics example |
| --- | --- | --- |
| **Automation** | AI performs a defined task you specify | "Convert this list of state names to two-letter codes." |
| **Augmentation** | You and AI work together as thinking partners | Brainstorming why survival rates on the Titanic differed by class, then testing the ideas yourself |
| **Agency** | AI acts with some independence on your behalf, often using tools | An AI agent that pulls data, runs a query, and drafts a report for you to review |

Most analytics work is **augmentation**: the analyst stays responsible for the question, the judgment, and the final answer.

### The four competencies

| Competency | Key question | In data analytics |
| --- | --- | --- |
| **Delegation** | Should AI do this, which parts, and with which tool? | Let AI draft the SQL; keep the decision about which records count as duplicates |
| **Description** | Have I clearly described the goal, context, and expected output? | Give the table name, column names, data types, and an example of the problem |
| **Discernment** | Is the output accurate, complete, and well reasoned? | Run the query, check row counts, compare with what you know to be true |
| **Diligence** | Am I using AI responsibly, transparently, and accountably? | Keep personal data out of the prompt, disclose AI use, own the final result |

The competencies form a loop. Weak results from Discernment usually send you back to Description (a clearer prompt) or Delegation (a different task split or tool).

![Infographic: the 4D AI Fluency Loop. Three circles form a cycle inside a dashed ring labeled Diligence: responsible use at every step. Delegation (Should AI do this?) leads to Description (Did I explain it clearly?) by handing off a task AI is suited for. Description leads to Discernment (Is the output right?) as the AI produces output. From Discernment, a weak result loops back to Description to write a clearer prompt, and a wrong task split or tool loops back to Delegation to re-delegate. A good result exits to Use the result and disclose it with an AID statement. Below the ring: Protect data, Check for bias, Disclose AI use, Own the result.](https://canvas.lorainccc.edu/courses/96040/files/15017257/preview)

### Applying the 4Ds: the census data cleaning problem

Recall the SQL data cleaning exercise in Module 3: the census table had a duplicate Hocking County record, and some states were entered as "OHIO" instead of "OH".

1. **Delegation:** Writing the SQL to find duplicates and inconsistent codes is a good task to delegate, because it is well defined and easy to check. Deciding which duplicate record to keep, and whether a record is truly a duplicate, stays with you.
2. **Description:** Tell the AI the table name, the relevant columns and their meaning, the database (MySQL), and the exact output you want, such as "a query that lists each `unique_county_code` appearing more than once, with its count."
3. **Discernment:** Run the query. Does it find Hocking County? Does the number of rows match what you found in Module 3? Did it accidentally group on the wrong column?
4. **Diligence:** The census data is public, so it is safe to share column names and sample rows. Note in your work that AI helped write the query, and confirm you understand every line before using it.

### Check your understanding

1. Classify each as automation, augmentation, or agency: (a) asking AI to reformat a date column; (b) discussing with AI possible reasons a t-test was not significant; (c) an assistant that automatically emails a weekly sales report.
2. For the Module 9 Data Governance Scorecard assignment, name one task you would delegate to AI and one you would not. Explain why.
3. Which of the four competencies is most often skipped by new AI users, and what is the risk?
