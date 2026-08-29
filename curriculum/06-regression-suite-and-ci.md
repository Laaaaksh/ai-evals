# Stage 6 — Regression suite and CI

**You'll be able to:** turn a real, diagnosed production failure into a
permanent, CI-blocking test - the practice sometimes called a "data
flywheel" - and explain why a regression suite protects against
*specific, known* bugs recurring, not against bugs nobody has found yet.

**Time:** 2–3 hours.

**Build:** [`code/06-regression-suite-ci`](../code/06-regression-suite-ci).

## Read, in this order

1. **[Braintrust, "How to turn LLM production failures into regression tests"](https://www.braintrust.dev/articles/turn-llm-production-failures-into-regression-tests)**
   (2026-05-29) - the concrete 5-step workflow this stage's sample is a
   small, self-contained version of: capture a failure, diagnose it,
   freeze it into a test case, write an assertion, gate releases on it.
2. **[`Jwuthri/Tracely-ai`](https://github.com/Jwuthri/Tracely-ai)** - skim
   the README. A real (if young - about 3 months old as of this writing)
   open-source attempt at automating the capture-and-freeze step this
   stage does by hand. Worth knowing exists, not required for this stage.

## Do

```bash
cd code/06-regression-suite-ci
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest test_regressions.py -v
```

All four tests should pass. Then do the exercise in
[`code/06-regression-suite-ci/README.md`](../code/06-regression-suite-ci/README.md)
that actually makes this stage's point instead of just describing it:
reintroduce one of the two documented historical bugs with a single `sed`
command, re-run `pytest`, and watch *exactly one* test fail - with the
original incident's explanation printed straight into the assertion
message. Then reintroduce the other one, confirm it isolates to the other
single test, and revert both. A regression suite where fixing one thing
breaks three unrelated tests teaches people to stop trusting red CI, which
is worse than having no suite - this stage's suite was specifically
verified not to do that.

## Checkpoint

You should be able to answer, without looking anything up:

- What does `regression_cases/case_002_short_numeric_id.json`'s
  `why_this_case_exists` field protect against, specifically - not "a bug,"
  but which exact line of code and which exact input?
- Why does `test_regressions.py` enforce that every case has a real
  `why_this_case_exists` explanation, rather than just checking
  input/output pairs?
- A regression suite passing tells you three specific old bugs haven't
  come back. What does it *not* tell you about the system's current
  quality? (If your answer references Stages 1 or 2, you're on the right
  track.)

Next: [Stage 7 — Where this sits now](07-where-this-sits-now.md).
