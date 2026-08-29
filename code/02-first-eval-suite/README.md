# 02 — Building a first eval suite

A small, from-scratch eval framework ([`eval_suite.py`](eval_suite.py)) run
over 15 cases ([`cases.jsonl`](cases.jsonl)) against fixed, pre-recorded
system outputs ([`fixture_outputs.jsonl`](fixture_outputs.jsonl)). The task
under test: extract `order_id`, `intent`, and `sentiment` from a support
message as JSON - a stand-in for the enormous share of real agent evals that
are really about structured-output correctness, not prose quality.

Companion to [`curriculum/02-first-eval-suite.md`](../../curriculum/02-first-eval-suite.md).

## Run it

```bash
python3 run_eval.py cases.jsonl fixture_outputs.jsonl --fail-under 0.9
```

No API key needed - this runs entirely against the pre-recorded fixture
outputs. You'll see a pass/fail grid across seven checks for all 15 cases,
then an aggregate pass rate, then a non-zero exit code because the fixture
outputs deliberately don't clear 90%.

Try a couple of thresholds:

```bash
python3 run_eval.py cases.jsonl fixture_outputs.jsonl --fail-under 0.5   # passes (exit 0)
python3 run_eval.py cases.jsonl fixture_outputs.jsonl --fail-under 0.95  # fails (exit 1)
```

That exit-code contract - pass under a threshold, fail over it - is exactly
what turns an eval suite into a CI gate. [Stage 6](../06-regression-suite-ci)
builds directly on this.

## The seven checks, and what each one is really testing

| Check | Kind | Catches |
|---|---|---|
| `valid_json` | binary | Output isn't parseable JSON at all (see `c05`) |
| `has_required_fields` | binary | JSON parses, but a field is missing (see `c08`) |
| `intent_in_enum` | binary | `intent` isn't one of the four allowed values (see `c09`) |
| `sentiment_in_enum` | binary | Same, for `sentiment` |
| `order_id_correct` | binary, exact match | Extracted the wrong order ID (see `c13`) |
| `intent_correct` | binary, exact match | Extracted the wrong intent |
| `sentiment_correct` | **graded**, not binary | Distinguishes an adjacent miss (`frustrated` vs. `angry`, see `c04`) from a hard miss (`angry` vs. `neutral`, see `c15`) - both fail the check, but the message tells you which kind of wrong it was |

Read [`eval_suite.py`](eval_suite.py) - it's under 130 lines, and the whole
point of this sample is that you can hold the entire mechanism in your head:
a check is a function from `(case, output)` to pass/fail plus a reason nothing
more. Real frameworks (promptfoo, DeepEval - see
[`resources/curated-resources.md`](../../resources/curated-resources.md))
add config file formats, parallelism, and a lot of built-in checks, but the
core idea is this.

## Try this

- Run it, then open `fixture_outputs.jsonl` and look at `c05`, `c08`, `c09`,
  `c13`, `c15` next to the failure messages you saw. Confirm you understand
  *why* each one failed before moving on.
- Add an eighth check: `intent_correct` currently gives no credit for a
  "close" wrong answer the way `sentiment_correct` does. Should it? Try
  writing a graded version and see whether it changes your read of which
  cases are actually broken versus borderline.
- Break something on purpose: edit one fixture output to be technically
  valid JSON but semantically wrong in a new way (e.g., an order ID that's
  the right *format* but the wrong order), and confirm the suite catches it.

## `--live`

```bash
python3 run_eval.py cases.jsonl --live
```

Calls a real model (via [`../common/llm_client.py`](../common/llm_client.py))
with a real extraction prompt instead of reading `fixture_outputs.jsonl`.
Requires `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`. This is optional - the
default (no `--live`) is what's verified to run in this repo's CI, and needs
no key, no network, and no spend.
