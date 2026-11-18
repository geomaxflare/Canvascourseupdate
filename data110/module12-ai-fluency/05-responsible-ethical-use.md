# Part 5 - Responsible and Ethical Use

### Purpose

Every AI shortcut carries a responsibility that stays with you. **Diligence** means protecting the people whose data you handle, following your organization's rules, being honest about how AI contributed, and owning the final result.

**After this page, you will be able to:** identify information that must not be entered into AI tools, recognize bias risks in AI output, identify types of bias, and write an AID statement to disclose AI use.

### Protect sensitive data

Text you enter into an AI tool may be stored, reviewed, or used to improve the service, depending on the tool and its settings. Sinclair's [Privacy Guide for AI Use](https://www.sinclair.edu/sites/www/assets/File/Hom-Aca-AcaDiv-eLearn/PrivacyGuideforAIUse.pdf) puts it simply: if you would not post it publicly, do not enter it into AI. Its three guidelines are to avoid sharing sensitive information, to use only tools approved by your institution, and to follow your organization's privacy policies.

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

AI models learn from human-generated data and can repeat its biases, as in the recidivism case study from Module 7. Sinclair's [How to Identify and Analyze Bias](https://www.sinclair.edu/sites/www/assets/File/Hom-Aca-AcaDiv-eLearn/BiasChecklist.pdf) checklist describes six types:

| Type | What it means | Analytics example |
| --- | --- | --- |
| **Sampling bias** | Training data does not represent all groups | A model trained mostly on urban data performs poorly for rural counties |
| **Annotation bias** | Human labelers' biases shape the labels | Inconsistent labels for "high-risk" customers |
| **Algorithmic bias** | The model's design favors certain outcomes | A scoring formula that overweights one variable |
| **Cultural bias** | Language and examples reflect one culture's viewpoint | Examples and assumptions that fit only U.S. norms |
| **Confirmation bias** | The AI reinforces what the user already believes | Agreeing with your hypothesis instead of testing it (Part 4, sycophancy) |
| **Systemic bias** | The AI mirrors historical inequalities | Using zip code or police contact as a proxy for race |

Before using AI output that describes or affects people, ask the checklist's four questions:

1. **Representation:** Who is included, excluded, or stereotyped?
2. **Perspective:** Whose viewpoint dominates the response?
3. **Fairness:** Does it treat all groups equally and respectfully?
4. **Impact:** Could it reinforce harmful stereotypes?

### Be transparent: the AID statement

Disclose how AI contributed to your work. Sinclair uses the **Artificial Intelligence Disclosure (AID) Framework** (Weaver, 2024). An AID statement has three parts ([AID Framework job aid](https://www.sinclair.edu/sites/www/assets/File/Hom-Aca-AcaDiv-eLearn/AIDFramework-Acknowledging.pdf)):

| Part | What to include |
| --- | --- |
| **AI tool(s) used** | The tool, its version or the date used, and the company |
| **Purpose of use** | What you used it for, such as writing code, explaining an error, or drafting text |
| **Human oversight** | How you reviewed, verified, and edited the output, and that you take responsibility for it |

Example for this course:

*"AI Tool: Microsoft Copilot (Microsoft), used November 2026. Purpose: I used Copilot to draft the SQL queries in Part B and to suggest wording for my summary. Human Oversight: I ran and verified every query against the census table, revised the summary, and take full responsibility for the accuracy of this work."*

Transparency lets others judge your work correctly, and undisclosed AI use may violate academic integrity policies.

### Use AI mindfully

AI systems use significant computing power and energy (see [Explained: Generative AI's environmental impact](https://news.mit.edu/2025/explained-generative-ai-environmental-impact-0117) from MIT, recommended by Sinclair). Keep prompts concise and purposeful, refine an existing conversation instead of starting over for similar questions, and avoid requesting unnecessarily long outputs.

### Accountability

If an AI-generated error reaches a report, the analyst is accountable, not the tool. "The AI said so" is never an acceptable explanation for a wrong number. Keep records of your prompts and checks for important work, so you can show how a result was produced.

### Check your understanding

1. A classmate pastes their employer's customer list into a free chatbot to get help cleaning it. What risks does this create, and what should they have done?
2. Write an AID statement for a project in which AI explained an R error message and suggested a chart type.
3. An AI suggests using "neighborhood" as a predictor in a model that decides who gets a loan. Which type of bias could this introduce? Answer the four bias analysis questions.
