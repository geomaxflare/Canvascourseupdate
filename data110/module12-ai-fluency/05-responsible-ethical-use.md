# Part 5 - Responsible and Ethical Use

### Purpose

Every AI shortcut carries a responsibility that stays with you. **Diligence** means protecting the people whose data you handle, following your organization's rules, being honest about how AI contributed, and owning the final result.

**After this page, you will be able to:** identify information that must not be entered into AI tools, recognize bias risks in AI output, disclose AI use appropriately, and apply a simple ethical check before using AI-assisted work.

### Protect sensitive data

Text you enter into an AI tool may be stored, reviewed, or used to improve the service, depending on the tool and its settings. Treat every prompt as if it could be seen by others.

| Never enter into a public AI tool | Why | Safer alternative |
| --- | --- | --- |
| Student records: names, IDs, grades, schedules | Protected by FERPA (Module 9) | Use made-up sample rows with the same columns |
| Health information | Protected by HIPAA | Describe the structure, not the records |
| Customer or employee personal data | Privacy laws and company policy | Remove or mask identifiers first |
| Passwords, API keys, connection strings | Security risk | Replace with placeholders such as `YOUR_PASSWORD` |
| Confidential business data | Contracts and competitive risk | Use an organization-approved tool, if one exists |

The census, `mtcars`, `ToothGrowth`, and taxi data used in this course are public and safe to share. When you are unsure, share **column names and data types, not data**.

### Follow policy

Organizations increasingly have AI policies that specify which tools are approved, what data may be used, and when AI use must be disclosed. In this course, follow the AI guidance in the syllabus and on each assignment. In the workplace, ask your manager or IT department before using AI with company data; this connects directly to the data governance practices from Modules 9 and 10.

### Watch for bias

AI models learn from human-generated data and can repeat its biases, as in the recidivism case study from Module 7. In analytics, watch for:

- suggestions to use variables that act as proxies for protected characteristics, such as zip code standing in for race;
- summaries that stereotype groups or describe them unequally;
- default examples and assumptions that fit some populations and not others.

Discernment and Diligence work together here: check outputs for bias, and do not let an AI make decisions about people without human review.

### Be transparent

Disclose how AI contributed to your work. A short **AI use statement** is enough:

*"I used Microsoft Copilot to draft the SQL query in Part B and to suggest wording for my summary. I ran and verified the query myself and revised the summary. All analysis decisions are my own."*

Transparency lets others judge your work correctly, and it is required in many academic and professional settings.

### An ethical check: the CARS model

Sinclair College's AI Institute uses the **CARS** model to guide ethical AI use. Before submitting or sharing AI-assisted work, ask:

| Step | Question to ask yourself |
| --- | --- |
| **Care** | Did I protect people's data and consider who could be affected by this work? |
| **Acknowledge** | Did I disclose how AI contributed? |
| **Review** | Did I verify the output and check it for errors and bias? |
| **Support** | Does the AI support my thinking and learning, rather than replace it? |

### Accountability

If an AI-generated error reaches a report, the analyst is accountable, not the tool. "The AI said so" is never an acceptable explanation for a wrong number. Keep records of your prompts and checks for important work, so you can show how a result was produced.

### Check your understanding

1. A classmate pastes their employer's customer list into a free chatbot to get help cleaning it. What risks does this create, and what should they have done?
2. Write an AI use statement for a project in which AI explained an R error message and suggested a chart type.
3. An AI suggests using "neighborhood" as a predictor in a model that decides who gets a loan. What concern should this raise?
