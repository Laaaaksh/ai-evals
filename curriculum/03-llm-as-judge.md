# Stage 3 — LLM-as-judge

**You'll be able to:** write a judge prompt for a genuinely subjective
task, validate it against human-labeled gold data, read Cohen's kappa and
TPR/FPR to know whether it's trustworthy, and calibrate it based on its
actual, specific misses - not a guess at what might be wrong.

**Time:** 3–5 hours - the longest stage in this curriculum, deliberately.
This is the hardest single skill in the whole curriculum to get right, and
the one most existing material treats too lightly.

**Build:** [`code/03-llm-judge`](../code/03-llm-judge).

## Read, in this order

1. **[Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"](https://arxiv.org/abs/2306.05685)**
   (2023-06-09) - the foundational paper. Read at least the sections on
   judge biases (position, verbosity, self-enhancement) - these are
   systematic, not noise, and no amount of gold-set validation alone fixes
   a systematically biased judge; you have to specifically test for them
   (e.g., swap answer order and see if the verdict flips).
2. **[Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators"](https://eugeneyan.com/writing/llm-evaluators/)**
   (2024-08-18) - the case for Cohen's kappa over raw accuracy, with real
   numbers. This is why `code/03` reports kappa as the headline metric, not
   just a pass rate.
3. **[Hamel Husain, "Using LLM-as-a-Judge For Evaluation: A Complete Guide"](https://hamel.dev/blog/posts/llm-judge/)**
   (2024-10-29) - "Critique Shadowing," a concrete 7-step calibration
   process. `code/03`'s v1 → v2 judge iteration is a small, mechanical
   version of exactly this process.
4. **[Rao & Callison-Burch, "Agreement Metrics for LLM-as-Judge Evaluation"](https://arxiv.org/abs/2606.00093)**
   (submitted 2026-05-25, revised 2026-07-31) - read after you've run
   `code/03` yourself. It shows reported judge-human agreement can range
   from 0.551 to 0.899 on the *same underlying task* purely from protocol
   choices - a useful corrective against over-trusting this stage's own
   kappa numbers, or anyone else's.

## Do

Run the comparison first, to see real, computed numbers before reading
anything else:

```bash
cd code/03-llm-judge
python3 run_judge.py --judge v1 --judge v2
```

Then read [`code/03-llm-judge/README.md`](../code/03-llm-judge/README.md)
in full - it walks through exactly why `judge_v1` (kappa 0.511, "moderate"
agreement) misses 43% of real hallucinations while never once wrongly
flagging a real grounded answer, why one calibration pass driven by reading
its actual misses raises `judge_v2` to kappa 0.742 ("substantial") and
catches 79%, and - just as important - which 3 cases even `judge_v2` still
gets wrong, and why fixing those needs real semantic understanding a
keyword heuristic structurally can't provide.

If you have `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` set, try:

```bash
python3 run_judge.py --judge v2 --live
```

and compare a real model's misses against `judge_v2`'s heuristic misses.
They won't be identical - sit with that, don't treat it as a bug.

## Checkpoint

You should be able to answer, without looking anything up:

- Why does this stage report Cohen's kappa instead of just accuracy? What
  specific number from `code/03`'s output would raw accuracy have hidden?
- Name one specific case `judge_v2` still gets wrong, and explain in your
  own words why a keyword-based heuristic can't fix it without becoming a
  fundamentally different kind of check.
- What's the difference between TPR and FPR, and why do you need both
  numbers - not just one - to trust a judge?

Next: [Stage 4 — Tracing and OpenTelemetry](04-tracing-and-otel.md).
