# Common pitfalls

The specific things that stop people, and the misconceptions almost everyone
starts with - collected here so you can check against this list before
assuming you've found a new problem.

## "We have observability" is not "we have evals"

The single most common confusion in this space, and the one with actual
survey data behind it: per a cited LangChain "State of Agent Engineering"
report (see
[`curated-resources.md`](curated-resources.md#ecosystem-direction---where-this-sits-now)),
89% of teams running agents in production report having *some*
observability, but under 40% report running online evals - and 29.5%
report no evaluation at all. Tracing (Stage 4) tells you *what happened*.
Evaluation (Stages 2-3) tells you *whether that was good*. A beautiful trace
waterfall showing a tool call, an LLM response, and a clean exit tells you
nothing about whether the response was actually correct - that's a judgment
call an eval, not a trace, has to make. Teams that stop at tracing have
visibility into a problem they still can't detect.

## Skipping straight to metrics, before doing error analysis

It's tempting to jump straight to "let's build an LLM judge" or "let's set
up a dashboard" before actually reading a pile of real transcripts by hand.
Resist this. [Stage 1](../curriculum/01-error-analysis.md) exists first in
this curriculum's sequence for a reason: a metric built before you've
actually seen what's failing tends to measure the failure mode you assumed
existed, not the one that's actually happening. Hamel Husain and Shreya
Shankar's error-analysis-first workflow (cited throughout
[`curated-resources.md`](curated-resources.md)) exists specifically because
teams that build dashboards first routinely discover, months later, that
the dashboard was tracking the wrong thing.

## Trusting raw accuracy on imbalanced data

If 85% of your eval set is "the agent did the right thing," a judge - or a
check, or a human reviewer - that says "yes" to everything scores 85%
accuracy while catching zero real failures. [Stage 3](../curriculum/03-llm-as-judge.md)'s
Cohen's kappa exists specifically to correct for this; see
`code/03-llm-judge/metrics.py` for a from-scratch implementation and
`code/03-llm-judge/README.md` for a worked example where two judges have
identical 0% false-positive rates but very different real catch rates
(TPR 57% vs. 79%) that raw accuracy alone would undersell.

## "Temperature 0" does not mean deterministic

A widely-held assumption that's simply wrong for both major providers as of
this writing. Anthropic's own docs state plainly that results aren't fully
deterministic even at `temperature=0.0`; OpenAI's `seed` parameter is
documented as best-effort, not a guarantee. The real mechanism (per
Thinking Machines Lab's 2025-09-10 research, cited in
[`curated-resources.md`](curated-resources.md#debugging-non-determinism)) is
a lack of *batch invariance* in GPU inference kernels, not floating-point
non-associativity as commonly assumed. If you're debugging a flaky agent
and you've already set `temperature=0`, that's not evidence the flakiness
must be coming from somewhere else - see
[Stage 5](../curriculum/05-debugging-nondeterminism.md).

## LLM judges have systematic biases, not just noise

Zheng et al.'s MT-Bench paper (2023, still the foundational citation for
this whole practice) catalogs specific, repeatable judge biases: **position
bias** (favoring whichever answer is shown first), **verbosity bias**
(favoring longer answers regardless of quality), and **self-enhancement
bias** (a model judging its own outputs more favorably than other models').
These aren't random noise you average away with a bigger gold set - they're
systematic, which means a judge can have a stable, non-trivial Cohen's kappa
against human labels *and* still be reliably wrong in one specific
direction. Check for these specifically (e.g., swap answer order and see if
the verdict flips) rather than assuming a good kappa number means the judge
has no blind spots.

## A judge validated once, never re-validated

[Stage 3](../curriculum/03-llm-as-judge.md)'s workflow - write a judge,
check it against gold data, fix what it misses - is not a one-time setup
step. EvalGen's "criteria drift" finding (Shankar et al., cited in
[`curated-resources.md`](curated-resources.md#llm-as-judge-methodology-and-calibration))
is that people's own criteria for "good" shift as they see more examples,
and a judge calibrated against last month's criteria silently drifts out of
alignment with this month's. Re-run the calibration check periodically
against fresh gold examples, not just once at launch.

## Trusting a small regression suite to mean "safe"

[Stage 6](../curriculum/06-regression-suite-and-ci.md)'s regression suite
(`code/06-regression-suite-ci`) protects against three *specific, known*
bugs recurring - it says nothing about bugs nobody has found yet. A green
CI run on a 3-case regression suite is not the same claim as "this system
works." Treat a regression suite as a ratchet that only ever tightens (each
real production failure adds one more permanent case), not as a substitute
for the broader eval suite from Stage 2 or ongoing error analysis from
Stage 1.

## Confusing "self-hosted" with "open source," and "open source" with "OSI-approved"

Covered in detail in
[`curated-resources.md`](curated-resources.md#tracing-and-observability-vendor-tools),
but worth restating here because it's an easy trap: Arize Phoenix is
commonly called open source and is genuinely free and self-hostable, but its
license (per GitHub's own classification, not independently confirmed
against the LICENSE file text in this research) is understood to be a
source-available license, not an OSI-approved one - a real distinction if
license terms matter for your use case. Braintrust and LangSmith are closed-
source SaaS products with only their client SDKs open-sourced; self-hosting
either is real but gated to their most expensive tier. Check a tool's actual
license and actual self-host tier, not its marketing language, before
depending on it.

## Expecting the OTel GenAI attribute names to be stable

Every `gen_ai.*` span and attribute in the OpenTelemetry GenAI semantic
conventions is marked **`Status: Development`**, not Stable, as of the spec
version this repository's [Stage 4](../curriculum/04-tracing-and-otel.md)
was built and verified against (checked 2026-08-27/29 - see
[`curated-resources.md`](curated-resources.md#opentelemetry-genai-semantic-conventions)).
Expect attribute names and structures to change before 1.0. This repo's own
`code/04-tracing-otel` sample states the exact spec version it was checked
against for exactly this reason - if you're reading this months later,
re-check the spec's current maturity status before assuming the attribute
names here still match it exactly.

## Toolchain: which key, which package

- `code/02` and `code/03`'s `--live` flag, and `code/04`'s optional real-
  backend export, need `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` - see
  `code/common/llm_client.py`. Every sample's *default* path needs neither.
- `code/04-tracing-otel` needs `opentelemetry-api`/`opentelemetry-sdk`
  (pinned versions in its `requirements.txt`); `code/06-regression-suite-ci`
  needs `pytest`. Every other sample needs only the Python standard library.
- If a `pip install` inside a sample's directory fails with an
  "externally-managed-environment" error on macOS/Homebrew Python, that's
  [PEP 668](https://peps.python.org/pep-0668/) - use a virtual environment
  (`python3 -m venv .venv && source .venv/bin/activate`) rather than
  `--break-system-packages`, which risks your system Python installation.
