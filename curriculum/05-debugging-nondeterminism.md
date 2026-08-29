# Stage 5 — Debugging non-determinism

**You'll be able to:** isolate whether a flaky agent failure is driven by
prompt sensitivity, tool-call formatting, retrieval variance, or noise in
the grading step itself - and recognize the specific point where simple
correlational analysis stops being able to tell you.

**Time:** 2–3 hours.

**Build:** [`code/05-debug-nondeterminism`](../code/05-debug-nondeterminism).

## Read, in this order

1. **[Thinking Machines Lab (Horace He), "Defeating Nondeterminism in LLM Inference"](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)**
   (2025-09-10) - the real mechanism behind "temperature 0 isn't actually
   deterministic": a lack of batch invariance in GPU inference kernels, not
   floating-point rounding as commonly assumed. Read this before assuming
   you've already eliminated randomness by setting temperature to 0.
2. **[Anthropic, Messages API reference - `temperature`](https://platform.claude.com/docs/en/api/messages)**
   and **[OpenAI, Advanced usage guide - `seed`](https://developers.openai.com/api/docs/guides/advanced-usage)**
   - two short primary-source confirmations of the same point from each
   major provider's own docs.

## Do

```bash
cd code/05-debug-nondeterminism
python3 diagnose.py --trials 400 --reveal
```

This runs a simulated flaky agent 400 times on the identical input and
tries to diagnose *why* it fails, using only what you'd actually be able to
observe in a real investigation - not the ground-truth cause, which
`--reveal` shows you afterward, separately, so you can check the diagnosis
against it.

Read [`code/05-debug-nondeterminism/README.md`](../code/05-debug-nondeterminism/README.md)
closely - **the diagnosis is only half right, and that's the actual
lesson**. The script correctly isolates two near-deterministic causes
(retrieval variance, tool-call formatting - both show a 100% conditional
failure rate) but conflates a real, weaker signal (prompt sensitivity,
which only misfires 60% of the time it's present) with pure grading noise
in its "unexplained" bucket, because a single lift threshold can't tell
them apart from correlational data alone. This isn't a bug to route around
quietly - it's the honest limit of the method, and real flaky-agent
debugging hits it constantly.

## Checkpoint

You should be able to answer, without looking anything up:

- Why doesn't setting `temperature=0` guarantee two identical calls produce
  identical output?
- In `code/05`'s output, `retrieved_doc=stale` and
  `tool_call_malformed=True` both get flagged as suspects while
  `prompt_variant=v2` doesn't, even though all three are real causes. Why?
- What's the difference between a correlational check (what `diagnose.py`
  does) and a controlled experiment (forcing one factor to a fixed value
  and measuring the outcome), and which one would actually separate
  `prompt_sensitivity` from `judge_noise` in this stage's data?

Next: [Stage 6 — Regression suite and CI](06-regression-suite-and-ci.md).
