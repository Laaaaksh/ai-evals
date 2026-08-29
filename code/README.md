# Code samples

Six small, self-contained programs, one per curriculum stage. Every sample
runs against fixed, pre-recorded fixture data by default - **no API key, no
network call, no cost** - and every one of them is actually executed in this
repo's CI (`.github/workflows/ci.yml`) on every push, not just
compile-checked. Where a sample supports `--live` to call a real model
instead, that's opt-in and documented in its own README.

| # | Sample | Idea |
|---|--------|------|
| [01](01-error-analysis) | `analyze_taxonomy.py` | Open-code 24 transcripts into a failure-mode taxonomy; check for saturation |
| [02](02-first-eval-suite) | `eval_suite.py` / `run_eval.py` | Binary and graded checks, structured-output assertions, a CI-gating exit code |
| [03](03-llm-judge) | `run_judge.py` | LLM-as-judge from scratch, validated against a 115-row gold set with Cohen's kappa, TPR/FPR |
| [04](04-tracing-otel) | `agent.py` | A multi-step agent traced with OpenTelemetry GenAI semantic conventions |
| [05](05-debug-nondeterminism) | `diagnose.py` | Isolating which of four causes explains a flaky agent's failures - and where that isolation breaks down |
| [06](06-regression-suite-ci) | `test_regressions.py` | Freezing three real (synthetic) production bugs into a pytest suite CI runs on every push |

Each pairs with a stage in [`curriculum/`](../curriculum) - see the
"Companion to" link at the top of each sample's README.

## Running a sample

Every sample is self-contained in its own directory:

```bash
cd code/0N-sample-name
python3 -m venv .venv && source .venv/bin/activate   # only needed for 04 and 06, which have real deps
pip install -r requirements.txt                       # if a requirements.txt exists
python3 the_main_script.py                             # or: pytest, for 06
```

Stages 01, 02, 03, and 05 need nothing beyond the Python standard library.
Stage 04 needs `opentelemetry-api`/`opentelemetry-sdk`; Stage 06 needs
`pytest`. Neither needs an API key.

## `code/common/`

[`llm_client.py`](common/llm_client.py) is the one genuinely shared piece: a
~50-line, provider-agnostic wrapper used only by samples' optional `--live`
flag (Stages 02 and 03) to call a real model via `ANTHROPIC_API_KEY` or
`OPENAI_API_KEY`. It's never imported by default - every sample's default
path needs no key and makes no network call.

## Why fixture-first, not live-first

Real judge calls, real traces sent to a real backend, and real flaky-model
behavior are what these stages are ultimately about - but a repository that
requires an API key (and ongoing spend) just to verify a lesson landed
excludes exactly the reader this is written for. Every sample's fixture
data was constructed to have real, checkable signal - Stage 3's gold set has
a genuinely computed Cohen's kappa, Stage 5's flaky agent has a genuinely
reproducible failure distribution - not placeholder data standing in for a
result you're asked to take on faith. `--live` is there for when you want
to see the same method applied to a real model instead of this repo's
fixtures.
