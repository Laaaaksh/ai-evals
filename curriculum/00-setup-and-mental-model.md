# Stage 0 — Setup and mental model

**You'll be able to:** explain what "evals" and "observability" actually
mean, why they're not the same thing despite being used almost
interchangeably, and confirm your environment is ready for every later
stage.

**Time:** 1–2 hours.

**Build:** run one script from [`code/01-error-analysis`](../code/01-error-analysis)
unmodified, to confirm Python and your environment work. Nothing to write
yet.

## Read, in this order

1. **[Hamel Husain, "Your AI Product Needs Evals"](https://hamel.dev/blog/posts/evals/)**
   (2024-03-29). The original three-level framework - unit tests,
   human/model eval, A/B testing - and still the right first thing to read
   in this space. Aged in date, not in relevance.
2. **[Hamel Husain, "A Field Guide to Rapidly Improving AI Products"](https://hamel.dev/blog/posts/field-guide/)**
   (2025-03-24). Read the first third - the case for error analysis before
   anything else. You'll do this for real in Stage 1.
3. Skim the **"Ecosystem direction - where this sits now"** section of
   [`resources/curated-resources.md`](../resources/curated-resources.md).
   In particular: per a cited industry survey, most teams running agents in
   production have *some* observability but far fewer run actual evals.
   That gap - visibility without judgment - is the specific problem this
   whole curriculum is about closing.

## The one distinction that matters most

**Observability** (Stage 4) tells you *what happened*: which tools were
called, in what order, with what latency, and whether anything threw an
error. **Evaluation** (Stages 1-3, 6) tells you *whether what happened was
good*. A trace can show a clean, error-free run that nonetheless gave a
customer wrong information - tracing has no opinion on correctness, only on
what occurred. Conflating the two is the single most common mistake people
make starting out; see
[`resources/common-pitfalls.md`](../resources/common-pitfalls.md#we-have-observability-is-not-we-have-evals)
for the data behind it.

This curriculum deliberately does evaluation first (Stages 1-3) and
observability second (Stage 4), even though most teams build them in the
opposite order or only ever build the second. That's on purpose: error
analysis (Stage 1) doesn't need any tooling investment at all, just reading
transcripts by hand, and it's what tells you *what to build a check for* in
Stage 2 - building observability infrastructure before you know what you're
looking for tends to produce a beautiful dashboard nobody uses.

## Do

Confirm your environment:

```bash
python3 --version   # 3.10+ is fine; every sample here was written and verified against 3.14
cd code/01-error-analysis
python3 analyze_taxonomy.py reference_labels.csv
```

You should see a frequency table and a saturation curve print to your
terminal, with no errors. That's it - no API key needed for this or almost
anything else in this curriculum (see below).

If you want to try a sample's optional `--live` mode later (Stages 2 and
3), set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` now - but it's genuinely
optional, and every checkpoint in this curriculum can be completed without
it.

## Checkpoint

You should be able to answer, without looking anything up:

- In your own words, what's the difference between "we have tracing" and
  "we have evals"? Give an example of a failure tracing would catch but a
  naive eval wouldn't, and one an eval would catch but tracing wouldn't.
- Why does this curriculum teach error analysis (Stage 1) before it teaches
  an automated eval suite (Stage 2)?

Next: [Stage 1 — Error analysis](01-error-analysis.md).
