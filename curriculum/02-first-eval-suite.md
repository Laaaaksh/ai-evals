# Stage 2 — Building a first eval suite

**You'll be able to:** write binary and graded checks against structured
output, and wire an eval suite into a pass/fail exit code a CI pipeline can
gate on.

**Time:** 2–3 hours.

**Build:** [`code/02-first-eval-suite`](../code/02-first-eval-suite).

## Read, in this order

1. **[promptfoo docs, "Expected Outputs"](https://promptfoo.dev/docs/configuration/expected-outputs/)**
   (live, checked 2026-08-30) - skim the list of built-in assertion types
   (`equals`, `contains`, `regex`, `is-json`, tool-call validation). You're
   about to write a small version of several of these by hand;
   seeing the production-grade list first gives you a sense of how far
   `code/02`'s ~130-line framework is a simplification, not the full
   picture.
2. **[Anthropic, "Define success criteria and build evaluations"](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)**
   - the four grading methods (exact match, cosine similarity, ROUGE-L, LLM
   grading) and when each fits. `code/02` covers the first of these in
   depth; Stage 3 covers the last.
3. **[Hamel Husain, "Your AI Product Needs Evals"](https://hamel.dev/blog/posts/evals/)**
   (2024-03-29) - re-read the "Level 1: Unit Tests" section specifically if
   you skimmed it in Stage 0. That's exactly what this stage builds.

## Do

Read [`code/02-first-eval-suite/eval_suite.py`](../code/02-first-eval-suite/eval_suite.py)
end to end first - it's under 130 lines and the whole framework fits in
your head: a check is a function from `(case, output)` to pass/fail plus a
reason. Then run it:

```bash
cd code/02-first-eval-suite
python3 run_eval.py cases.jsonl fixture_outputs.jsonl --fail-under 0.9
```

Read the pass/fail grid and the failure messages against the actual fixture
outputs in `fixture_outputs.jsonl` - confirm you understand exactly why
each failing check failed before moving on. Full walkthrough in
[`code/02-first-eval-suite/README.md`](../code/02-first-eval-suite/README.md),
including the difference between this stage's binary checks and its one
graded check (`sentiment_correct`), and why a graded check can distinguish
a near-miss from a wildly wrong answer where a binary one can't.

## Checkpoint

You should be able to answer, without looking anything up:

- What's the difference between a binary check and a graded check, and
  name one thing in `code/02`'s task (order ID, intent, or sentiment
  extraction) that's a bad fit for a binary check?
- `run_eval.py --fail-under 0.9` exits non-zero on this stage's fixture
  data. What specifically would need to change in the *system under test*
  - not the eval suite - to make that number pass?
- Why does `valid_json` need to exist as its own separate check, rather
  than just letting `has_required_fields` fail on malformed input?

Next: [Stage 3 — LLM-as-judge](03-llm-as-judge.md).
