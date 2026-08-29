# Stage 1 — Error analysis

**You'll be able to:** read a set of real transcripts and open-code them
into a failure-mode taxonomy by hand, and recognize when you've coded
enough examples to trust that taxonomy (theoretical saturation).

**Time:** 2–3 hours.

**Build:** [`code/01-error-analysis`](../code/01-error-analysis) - code
your own labels for 24 transcripts before running anything.

## Read, in this order

1. **[Hamel Husain, "Evals: Doing Error Analysis Before Writing Tests"](https://hamel.dev/notes/llm/officehours/erroranalysis.html)**
   (2024-12-21). The concrete workflow this stage's sample is a small,
   runnable version of: read transcripts, write a short failure
   description for each, reuse a label when you've seen the same problem
   before.
2. **[Hamel Husain & Shreya Shankar, "LLM Evals: Everything You Need to Know"](https://hamel.dev/blog/posts/evals-faq/)**
   (published 2025-05-28, updated 2026-07-18) - read the section on open
   coding, axial coding, and theoretical saturation. The saturation curve
   `code/01`'s script prints is a direct implementation of the idea covered
   here.
3. **[Shreya Shankar et al., "Who Validates the Validators?" (EvalGen)](https://arxiv.org/abs/2404.12272)**
   (2024-04-18) - skim the introduction for "criteria drift": the finding
   that people's own sense of what counts as a failure shifts as they see
   more examples. This is why open coding comes *before* you commit to a
   fixed taxonomy, not after.

## Do

Open [`code/01-error-analysis/transcripts.json`](../code/01-error-analysis/transcripts.json)
and read all 24 transcripts - a synthetic customer-support agent handling
order status, refunds, and cancellations. For each one, write down: did the
agent get this right, and if not, what specifically went wrong, in your own
words. Reuse a label when you notice the same kind of problem twice.

Save your labels as a CSV, then run:

```bash
cd code/01-error-analysis
python3 analyze_taxonomy.py your_labels.csv
```

Compare against
[`reference_labels.csv`](../code/01-error-analysis/reference_labels.csv) -
full instructions in [`code/01-error-analysis/README.md`](../code/01-error-analysis/README.md).
Don't skip to the reference first; the exercise is in the noticing, not in
matching an answer key.

## Checkpoint

You should be able to answer, without looking anything up:

- What does "theoretical saturation" mean, and how would you know your own
  taxonomy hadn't reached it yet?
- Name two failure modes from the 24 transcripts that a simple "did the
  agent respond" check would completely miss.
- Why is a failure-mode taxonomy built *before* Stage 2's automated checks,
  rather than the other way around?

Next: [Stage 2 — Building a first eval suite](02-first-eval-suite.md).
