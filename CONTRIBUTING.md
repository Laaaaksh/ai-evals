# Contributing to ai-evals

Thanks for considering a contribution. This is a curriculum plus runnable
samples, open source under the MIT license.

## Getting started

```bash
git clone https://github.com/<your-username>/ai-evals.git   # your fork
cd ai-evals
```

Every sample lives in its own directory under `code/`. Most need nothing
beyond Python 3.10+ and the standard library:

```bash
cd code/01-error-analysis
python3 analyze_taxonomy.py reference_labels.csv
```

Two samples have real dependencies - install them in a virtual environment,
not system-wide:

```bash
cd code/04-tracing-otel      # or code/06-regression-suite-ci
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

No sample needs an API key by default. `code/02` and `code/03` support an
optional `--live` flag that does - see `code/common/llm_client.py`.

## Contribution workflow

1. Fork the repo, clone your fork (command above).
2. Create a descriptively named branch off `main`.
3. Make focused commits.
4. If you touched anything under `code/`, prove the sample(s) you changed
   still run - paste the actual command and output in the PR. If a sample
   has a `requirements.txt`, install and run it in a fresh virtual
   environment before claiming it works.
5. If you touched `resources/curated-resources.md`, open every link you're
   adding or changing and confirm it resolves before submitting. Never add
   a link you haven't personally opened, and never restate a star count,
   date, or claim from memory - check it live.
6. Open a pull request against `main`.

A PR can merge only when CI passes and review feedback is resolved. CI
actually runs every sample's default path - not just a syntax or compile
check - so a broken sample fails CI directly.

## What contributions are useful

- Fixing a wrong claim, a stale "current" statement, or a dead link.
- Reporting or fixing drift in a vendor's self-host instructions, pricing
  tier, or OpenTelemetry GenAI semantic-convention support - this is a
  fast-moving part of the industry (see
  [`curriculum/07-where-this-sits-now.md`](curriculum/07-where-this-sits-now.md))
  and this repo's claims will go stale faster than most.
- A new sample that isolates one concept the way the existing ones do (see
  "Adding a sample" below) - open an issue first so scope is agreed before
  you write it.
- Real numbers from running a sample's `--live` mode against a model - a PR
  or issue reporting how a real model's judge verdicts or extraction output
  compared to the fixture behavior described in that sample's README.
- Curriculum sequencing feedback: if a stage assumes something the previous
  stage didn't actually teach, that's a real bug in a course, not a
  nitpick.

## Adding a sample

Each directory under `code/` demonstrates exactly one idea. Follow the
existing pattern:

- Runs by default against fixed fixture data - no API key, no network call,
  no cost. An optional `--live` flag calling a real model is fine (see
  `code/common/llm_client.py`), but it must never be required to complete
  the curriculum stage the sample belongs to.
- A `README.md` explaining what the sample shows, what to look for in its
  actual output (paste real output, not a hypothetical), and how it
  connects to the curriculum stage that references it.
- Comments in the code explain *why* a line matters for the concept being
  taught, not what a standard library call does.
- If it needs dependencies beyond the standard library, a pinned
  `requirements.txt` and a line in this repo's
  `.github/workflows/ci.yml` that actually runs it.
- Prefer extending an existing stage's "Try this" exercises over adding a
  new curriculum stage - new stages change the sequencing for everyone.

## Code style

- Comments explain *why*, not *what*.
- No comments that just restate the line below them.
- Match the existing pattern in a directory rather than inventing a new
  one - e.g. `code/03-llm-judge`'s two-heuristic (`judge_v1`/`judge_v2`)
  calibration pattern, or `code/06-regression-suite-ci`'s
  `why_this_case_exists` field.

## Reporting issues

Open a GitHub issue before starting anything larger than a typo fix, so
scope is agreed first. Use the bug report template for something broken,
and the resource suggestion template for anything about
`resources/curated-resources.md`.
