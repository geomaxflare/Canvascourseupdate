# Part 6 - AI Across the Analytics Workflow

### Purpose

AI is useful at nearly every step of an analysis, but the right kind of help differs from step to step. This page maps AI uses onto the data analysis process you learned in Module 1, using examples from this course, and gives you a way to keep your skills current as tools change.

**After this page, you will be able to:** identify high-value uses of AI at each stage of an analysis, recognize the human decisions at each stage, and evaluate new AI tools as they appear.

### AI at each stage

| Stage | Good uses of AI | Course example | What stays with you |
| --- | --- | --- | --- |
| **Ask a question** | Brainstorm questions and hypotheses | "What questions could the Titanic data answer?" | Choosing the question that matters to the business |
| **Collect and read data** | Write import code; explain file formats | R `read_excel` code for the census file | Confirming the source is reliable and permitted |
| **Clean and wrangle** | Write SQL or R to find and fix problems | Finding "OHIO" values and duplicate counties | Deciding what counts as an error and how to fix it |
| **Visualize** | Suggest chart types; write ggplot2 or Power BI steps | A map of Ohio population by county | Checking that the chart is honest (Module 4's misleading visuals) |
| **Model and test** | Suggest a method; write and explain code | Choosing a paired t-test for `sleep` | Checking conditions and interpreting results |
| **Interpret** | Explain output in plain language | Explaining regression coefficients for car prices | Judging practical importance and limitations |
| **Communicate** | Draft summaries, emails, and slide text | A manager summary of a chi-square result | Accuracy, tone, and accountability for every claim |

### Automation versus augmentation in practice

- **Automate** repetitive, well-defined, easy-to-check tasks: reformatting, writing boilerplate code, converting units.
- **Augment** judgment-heavy work: choosing a method, interpreting results, deciding what to recommend. Use AI as a thinking partner, and make the decision yourself.
- **Do not delegate** decisions that affect people, such as grades, hiring, or loans, without careful human review and organizational approval.

### AI tools for analysts

Many tools you already use now include AI features: Copilot in Excel and Power BI, AI assistants in RStudio and other coding tools, and natural language query features in BI tools. The same 4D competencies apply to every one of them.

### Staying current

AI tools change every few months. Instead of memorizing features, build habits that transfer:

- **Test new tools on a problem you already know the answer to,** as you do in this module's assignment. It is the fastest way to see a tool's strengths and weaknesses.
- **Check each tool's data and privacy terms** before using it with real data.
- **Follow a few reliable sources,** such as your professional community, vendor documentation, and the AI resources published by colleges such as Sinclair's AI Institute.
- **Keep a prompt library** of prompts that worked well for recurring tasks; Sinclair's AI Cookbook is an example of this practice.

### Check your understanding

1. For the Market Basket Analysis assignment in Module 6, name one task you would give to AI and one you would keep for yourself.
2. Which stage of the analysis process benefits most from AI in your own experience so far? Which carries the most risk?
3. A new AI tool promises to "build dashboards automatically." Describe how you would test it before trusting it with work data.
