# Part 1 - What Generative AI Is and Isn't

### Purpose

You cannot judge an AI's answer without knowing how it produces one. This page explains, without math, what a large language model does, why it is so capable, and why it makes the specific kinds of mistakes it does.

**After this page, you will be able to:** explain how a large language model generates text, distinguish generative AI from the machine learning models you built in Modules 6 and 8, and list its main strengths and limitations.

### From the models you built to generative AI

In Module 6, you built regression models that predict a number (a car's price) from inputs (mileage and year). In Module 8, you used Orange to build classification models that predict a category. These are **predictive** machine learning models: trained on one dataset for one narrow task.

**Generative AI** creates new content: text, code, images, or audio. The AI assistants you will use in this module are powered by **large language models (LLMs)**, trained on enormous amounts of text to perform one deceptively simple task: **predict the next piece of text**.

| | Predictive ML (Modules 6 and 8) | Generative AI (LLMs) |
| --- | --- | --- |
| Output | A number or a category | New text, code, or images |
| Training data | One specific dataset | Vast amounts of general text and code |
| Task | One narrow prediction | Almost any language task |
| How to use it | Train and evaluate a model | Write a prompt |
| Main risk | Overfitting, biased training data | Fluent but false answers, biased or outdated content |

### How an LLM produces an answer

1. Your prompt is split into **tokens**, small chunks of text such as words or parts of words.
2. The model predicts which token is most likely to come next, based on patterns it learned during training.
3. It adds that token and repeats, one token at a time, until the answer is complete.

Several consequences follow directly from this design:

- **It predicts plausible text, not verified facts.** If a confident-sounding wrong answer is statistically likely, the model may produce it. Invented facts, citations, or numbers are called **hallucinations**.
- **It does not run your data unless it uses a tool.** Asked "what is the mean of this column?", a plain LLM may estimate a number instead of calculating it. Many assistants can now run code, but you should know whether yours did.
- **It has a knowledge cutoff.** Its training data ends at a point in time, so it may not know recent events, new software versions, or your organization's own data unless you provide them or it can search.
- **It is sensitive to wording.** Small changes in a prompt can change the answer, which is why Part 3 matters.
- **It reflects its training data,** including its biases, as you saw with the recidivism algorithm in Module 7.

### What it is good and bad at for analysts

| Usually strong | Often weak |
| --- | --- |
| Writing and explaining SQL, R, and Excel formulas | Arithmetic and statistics done "in its head" |
| Explaining error messages and concepts | Facts about specific, recent, or local information |
| Drafting summaries, emails, and report text | Knowing whether its own answer is correct |
| Suggesting chart types and analysis approaches | Your organization's definitions, data, and policies |
| Brainstorming questions and edge cases | Citing real sources accurately |

### Myths and facts

Sinclair College's AI Excellence Institute summarizes common misconceptions in [AI: Fears, Myths, and Facts](https://www.sinclair.edu/sites/www/assets/File/Hom-Aca-AcaDiv-eLearn/AIFearsMythsandFacts.pdf). Three matter most for analysts:

| Myth | Fact |
| --- | --- |
| AI is sentient and understands what it says | AI has no awareness; it generates text from patterns in its training data |
| AI knows everything | AI only knows what it was trained on or what you give it, and it still makes mistakes |
| AI is always objective and unbiased | AI can reflect the biases in its training data (Part 5) |

Keep Sinclair's [Glossary of AI Terms](https://www.sinclair.edu/sites/www/assets/File/Hom-Aca-AcaDiv-eLearn/AIGlossary.pdf) handy as you work through this module.

### Check your understanding

1. In one or two sentences, explain to a classmate why an LLM can write a convincing but false statistic.
2. You ask an assistant for the average population of Ohio's 88 counties and paste no data. What is the risk, and what should you do instead?
3. How is the Orange model you built in Module 8 different from the assistant you will use in this module?
