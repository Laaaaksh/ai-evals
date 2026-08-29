# The curriculum

Eight stages, in order. Each one names what you'll be able to do at the end,
what to read or watch, roughly how long it takes, and what to build to prove
it stuck. Do them in order the first time through - later stages assume
earlier ones, and the sequence itself (error analysis before metrics,
metrics before a judge, a judge before you trust it in a regression suite)
is the actual point of this repository, not incidental structure.

| Stage | You'll be able to... | Time | Build |
|---|---|---|---|
| [0 — Setup and mental model](00-setup-and-mental-model.md) | Explain what "evals" and "observability" each are, and why they're not the same thing | 1–2 hr | Run `code/01`'s script once, unmodified, to confirm your environment works |
| [1 — Error analysis](01-error-analysis.md) | Open-code real transcripts into a failure-mode taxonomy, and know when you've seen enough | 2–3 hr | `code/01-error-analysis` |
| [2 — First eval suite](02-first-eval-suite.md) | Write binary and graded checks, and wire them into a pass/fail CI gate | 2–3 hr | `code/02-first-eval-suite` |
| [3 — LLM-as-judge](03-llm-as-judge.md) | Build a judge, validate it against gold data, and read Cohen's kappa/TPR/FPR to know if it's trustworthy | 3–5 hr | `code/03-llm-judge` |
| [4 — Tracing and OpenTelemetry](04-tracing-and-otel.md) | Instrument an agent with OTel GenAI conventions and read the resulting trace | 2–4 hr | `code/04-tracing-otel` |
| [5 — Debugging non-determinism](05-debugging-nondeterminism.md) | Isolate whether a flaky failure is prompt sensitivity, tool formatting, retrieval variance, or judge noise - and know when you can't | 2–3 hr | `code/05-debug-nondeterminism` |
| [6 — Regression suite and CI](06-regression-suite-and-ci.md) | Freeze a real failure into a permanent, CI-blocking test | 2–3 hr | `code/06-regression-suite-ci` |
| [7 — Where this sits now](07-where-this-sits-now.md) | Choose a tracing/eval vendor for a real constraint, and know what's still moving under you | 1–2 hr | A written vendor decision for a scenario you pick |

**Total: roughly 15–25 hours** of focused work, spread over however long
that takes you. There's no clock running.

## Prerequisites

You should be comfortable writing and debugging Python - reading a regex,
running a script with a virtual environment, understanding a stack trace.
You do **not** need prior experience with evals, observability, or any
specific AI framework. If you've never called an LLM API, that's fine -
every sample's default path needs no API key at all (see
[Stage 0](00-setup-and-mental-model.md)).

## How each stage is structured

- **What to read or watch** - a short, sequenced list, not an unordered
  pile. Full annotated detail (what's covered well, how current it is, and
  what's stale but still worth it) lives in
  [`resources/curated-resources.md`](../resources/curated-resources.md) -
  each stage links the specific entries relevant to it.
- **What to build** - a runnable sample in [`code/`](../code), with its own
  README explaining what to look for. Every sample runs against fixed
  fixture data by default - no API key, no cost - and is actually executed
  in this repo's CI, not just described. Building it is not optional:
  Stage 3's calibration numbers, Stage 5's diagnostic gap, and Stage 6's
  isolated bug-catches are all real, computed output from running the code,
  not a hypothetical you're asked to take on faith.
- **Checkpoint questions** - answer these without looking anything up
  before moving on. They're not a quiz to pass, they're a way to notice
  what didn't actually land.

## If something stops you

[`resources/common-pitfalls.md`](../resources/common-pitfalls.md) collects
the specific things that stop most people starting out - the toolchain
issues, the "temperature 0 means deterministic" misconception, the trap of
trusting raw accuracy over Cohen's kappa on imbalanced data, and more.
Check there before assuming you've found a new problem.
