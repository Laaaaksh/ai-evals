<div align="center">

# ai-evals

**A sequenced path from "I shipped an agent" to "I can tell you whether it
actually works, and keep telling you" — with runnable code at every step.**

[![CI](https://github.com/Laaaaksh/ai-evals/actions/workflows/ci.yml/badge.svg)](https://github.com/Laaaaksh/ai-evals/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](code/README.md)

**[Curriculum](curriculum/README.md) • [Code samples](code/README.md) • [Resources](resources/curated-resources.md) • [Common pitfalls](resources/common-pitfalls.md) • [Contributing](CONTRIBUTING.md) • [License](LICENSE)**

</div>

## What this is

AI eval and observability material isn't scarce - Hamel Husain's notes,
vendor docs from Langfuse and half a dozen competitors, a paid Maven cohort
that's trained thousands of people, academic papers on judge calibration.
What's missing is a **path**: something that sequences error analysis
before metrics, metrics before a judge, a judge before you trust it in a
regression suite - and tells you, plainly, when a resource has aged or a
tool has changed hands. An unordered list of links is the problem this repo
exists to not be.

This repo is eight sequenced stages, each with:

- **What you'll be able to do** at the end of it, stated concretely.
- **What to read**, in order - a handful of things, not a pile, with the
  full reasoning in
  [`resources/curated-resources.md`](resources/curated-resources.md).
- **A small, complete, commented program to run**, in [`code/`](code) -
  open-coding real transcripts into a failure taxonomy, a from-scratch eval
  suite with a CI-blocking exit code, an LLM judge calibrated against a
  115-row gold set with a real, computed Cohen's kappa, an agent traced
  with OpenTelemetry's GenAI conventions, a flaky agent whose failure cause
  you have to diagnose from observable signals alone, and three real
  (synthetic) production bugs frozen into a pytest suite this repo's own
  CI runs on every push.
- **Checkpoint questions** to answer before moving on.

Start at [`curriculum/README.md`](curriculum/README.md).

## What this repository does not cover

This stops at the core loop for a single agent: error analysis, a first
eval suite, an LLM judge, tracing, non-determinism, and a regression suite.
It does not cover multi-agent coordination evaluation, red-teaming or
adversarial robustness testing (promptfoo has real depth here - see
[`resources/curated-resources.md`](resources/curated-resources.md)), or
RAG-specific metrics beyond the grounding-judge task in Stage 3 (ragas is
the deeper resource for that). [Stage
7](curriculum/07-where-this-sits-now.md) covers where to go from here and
how to pick a tracing/eval vendor for a real constraint, not just the most
popular one.

## No API key required — read this before anything else

**Every sample in this repo runs by default against fixed, pre-recorded
fixture data - no API key, no network call, no cost - and every one is
actually executed in this repo's CI on every push, not just described.**
Stage 3's Cohen's kappa numbers, Stage 5's diagnostic gap, and Stage 6's
isolated-bug-catch behavior are all real, computed output from running the
code in this repository, verified while writing it - not a hypothetical
result asked to be taken on faith.

Two samples optionally support `--live`, to call a real model instead of
fixtures ([Stage 2](curriculum/02-first-eval-suite.md) and [Stage
3](curriculum/03-llm-as-judge.md)) - set `ANTHROPIC_API_KEY` or
`OPENAI_API_KEY` if you want to try it. Stage 3's `--live` run makes about
115 API calls against the gold set; expect low-single-digit dollars, not
more. This is genuinely optional - every checkpoint in this curriculum can
be completed without spending anything. Full detail in [`code/README.md`](code/README.md#why-fixture-first-not-live-first).

## Repository layout

```
curriculum/   8 sequenced stages - the path itself
code/         6 runnable, commented samples (stages 1-6; stages 0 and 7 are read/write-only)
resources/    honest, dated curation of everything external cited above
```

## Contributing

Contributions are welcome - a wrong claim, a stale "current" statement, a
dead link, real numbers from running a sample's `--live` mode against a
model. See [CONTRIBUTING.md](CONTRIBUTING.md). Please read
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) first.

## Security

Found a security issue? See [SECURITY.md](SECURITY.md) - please don't open
a public issue for it.

## License

MIT - see [LICENSE](LICENSE).
