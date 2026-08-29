# 06 — Regression suite: freezing production failures into CI-blocking tests

Three JSON files under [`regression_cases/`](regression_cases), each a real
(synthetic) production bug that was found, diagnosed, and fixed - and a
pytest suite ([`test_regressions.py`](test_regressions.py)) that turns each
one into a permanent test. This is the "data flywheel" idea from
[`curriculum/06-regression-suite-and-ci.md`](../../curriculum/06-regression-suite-and-ci.md):
every real failure you fix becomes coverage that stops it from silently
coming back, gated in CI the same way this repo's own
[`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) runs this exact
suite on every push.

This is the one sample in this repo that's a genuine, always-executed
pytest suite in CI - not a script whose output gets pasted into a README.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest test_regressions.py -v
```

```
test_regressions.py::test_regression_case[case_001_lowercase_order_id] PASSED
test_regressions.py::test_regression_case[case_002_short_numeric_id] PASSED
test_regressions.py::test_regression_case[case_003_negated_sentiment] PASSED
test_regressions.py::test_every_case_has_a_reason PASSED
```

[`system_under_test.py`](system_under_test.py) is a small, rule-based (not
LLM-based) version of Stage 2's extraction task - deliberately simple, so
you can point at the exact line each historical bug lived on. Each case in
`regression_cases/*.json` has an `id`, the exact `input` that broke
production, the `buggy_output` that was observed at the time, the `expected`
output now required, and a `why_this_case_exists` explanation - a
regression case with no recorded reason is a case nobody can safely remove
later (`test_every_case_has_a_reason` enforces the field exists).

## Try this: reintroduce a real bug and watch it get caught

Each case corresponds to one specific, isolated line in
`system_under_test.py`. Break one, run the suite, watch exactly one test
fail - then look at the failure message, which quotes the original
incident back at you:

```bash
# case_001: narrow the letter class back to uppercase-only
sed -i '' 's/\[A-Za-z\]\\d{4}/[A-Z]\\d{4}/' system_under_test.py
pytest test_regressions.py -v
# -> only case_001_lowercase_order_id fails, with the original bug's
#    explanation printed in the assertion message
git checkout system_under_test.py   # or manually revert the sed
```

```bash
# case_002: raise the minimum digit count back to 4
sed -i '' 's/\\d{2,}/\\d{4,}/' system_under_test.py
pytest test_regressions.py -v
# -> only case_002_short_numeric_id fails
git checkout system_under_test.py
```

Both were verified independently while building this sample: each edit
breaks exactly the one case it corresponds to, not the others - that's what
makes a regression suite useful instead of noisy. A suite where fixing one
thing breaks three unrelated tests teaches people to stop trusting red CI,
which is worse than having no suite at all.

## Try this too

- Add a fourth regression case for a bug you find yourself: change
  `extract_intent` or `extract_sentiment` in some plausible way, notice
  what breaks, then write it up as a `case_004_*.json` the same way the
  other three are documented - `input`, `buggy_output`, `expected`,
  `why_this_case_exists` - before fixing the code back.
- `test_regressions.py` currently asserts exact field equality. Real
  regression suites often need the graded/partial-credit style checks from
  [Stage 2](../02-first-eval-suite) instead of exact match - try wiring
  `eval_suite.py`'s `sentiment_correct` check into this suite instead of a
  plain `==`.
- Look at how this suite is invoked in
  [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) - it's a
  normal `pytest` call, no special CI-only logic. That's deliberate: a
  regression suite that only works in CI, or only works locally, isn't
  trustworthy either way.
