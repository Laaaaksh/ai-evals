# 05 — Debugging non-determinism

A simulated agent ([`flaky_agent.py`](flaky_agent.py)) that fails for four
different, specific reasons - prompt sensitivity, retrieval variance,
tool-call formatting, and grading/judge noise - run 400 times on the same
input, then diagnosed using only what you'd actually be able to observe in
a real flaky-agent investigation: prompt wording, which document got
retrieved, whether the tool call parsed. Not the ground-truth cause - that's
revealed separately, afterward, the same "diagnose first, check your answer
second" structure as Stage 1.

Companion to [`curriculum/05-debugging-nondeterminism.md`](../../curriculum/05-debugging-nondeterminism.md).

## Run it

```bash
python3 diagnose.py --trials 400 --reveal
```

This is the actual output from this repo's fixture agent - not hypothetical:

```
400 runs of the same input, same seed policy - 161 failed (40.2%)

By prompt_variant:
  v1         n=155  fail_rate=25.2%
  v2         n=122  fail_rate=60.7%
  v3         n=123  fail_rate=39.0%

By retrieved_doc:
  current    n=344  fail_rate=30.5%
  stale      n=56   fail_rate=100.0%  <- 2.5x baseline, SUSPECT

By tool_call_malformed:
  False      n=364  fail_rate=34.3%
  True       n=36   fail_rate=100.0%  <- 2.5x baseline, SUSPECT

Suspect factor values: {'retrieved_doc': {'stale'}, 'tool_call_malformed': {True}}
86/161 failures explained by a suspect input factor.
75/161 failures are NOT explained by any input factor tested...

--- ground truth (for checking the diagnosis above) ---
  retrieval_variance     50 (12.5% of all runs)
  prompt_sensitivity     50 (12.5% of all runs)
  tool_format            36 (9.0% of all runs)
  judge_noise            25 (6.2% of all runs)
```

## Read this carefully - the diagnosis is only half right, on purpose

The script correctly isolates `retrieval_variance` and `tool_format`: both
show a **100% conditional failure rate** - every single run with a stale
doc or a malformed tool call failed, a huge, unambiguous signal. Those two
suspects account for 86 of 161 failures - exactly the 50 + 36 the ground
truth attributes to retrieval and tool-format respectively (see
`flaky_agent.py`: the two never overlap in a single run, by construction).

The 75 "unexplained" failures are **not** one thing - the ground truth
reveals they're two: 50 from `prompt_sensitivity` and 25 from
`judge_noise`, mixed together. Why didn't the script separate them? Look at
the `prompt_variant` table again: `v2` really is elevated (60.7% vs. a
40.2% baseline - a real, 1.5x signal) but it doesn't clear this script's
`LIFT_THRESHOLD = 2.0`, so it's never flagged as a suspect and its failures
land in "unexplained" alongside the genuinely unrelated judge noise.

**This is the actual, honest limit of this diagnostic method, not a bug to
fix quietly**: a threshold-based correlational check catches strong,
near-deterministic factors well (retrieval, tool format) and is bad at
separating a real-but-partial factor (prompt sensitivity, which only
confuses the agent 60% of the time it's even present) from pure noise
(judge flakiness) when both end up in the same leftover bucket. Real
flaky-agent debugging has exactly this problem: correlation on observational
data (just watching what happens to vary) can miss weaker real causes and
conflate them with noise you can't fix by looking at the input at all.

## Try this

- Lower `LIFT_THRESHOLD` in `diagnose.py` to `1.4` and re-run. `v2` gets
  flagged now - but check whether that changes the *unexplained* count in a
  way that still doesn't perfectly separate `prompt_sensitivity` from
  `judge_noise`. A single global threshold can't fully solve this; that's
  the point.
- Design and implement a better test: instead of passively observing which
  `prompt_variant` a random run happened to get, **force** `prompt_variant`
  to a fixed value across many trials (a controlled experiment, not an
  observational one) and measure the failure rate difference directly. This
  is the real technique - vary exactly one factor while holding everything
  else fixed - that separates correlation from causation, which pure
  observational lift-flagging (what this script does) structurally can't do
  on its own.
- `judge_noise` here means "the grading step was wrong about a correct
  answer" - the single hardest failure mode to diagnose from outside,
  because by definition nothing about the *input* explains it. Stage 3
  covers measuring a judge's own reliability directly (Cohen's kappa,
  TPR/FPR against a gold set) rather than inferring judge noise indirectly,
  as this script has to.
