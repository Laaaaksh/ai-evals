# 03 — LLM-as-judge, from scratch

The task: given a policy snippet and a support agent's response, judge
whether the response is **grounded** (every claim traces back to the
snippet) or **ungrounded** (it states a fabricated number, condition, or
scope). This is the exact shape of the most common real judge task -
RAG "faithfulness" / hallucination detection - kept small enough to hold in
your head.

Companion to [`curriculum/03-llm-as-judge.md`](../../curriculum/03-llm-as-judge.md).

## The gold set

[`gold_labels.csv`](gold_labels.csv) - 115 rows, built by
[`generate_gold_set.py`](generate_gold_set.py) from 23 hand-written
(snippet, response) pairs across 5 policy areas, each wrapped in 5 different
conversational openers. **This is synthetic data, not scraped real
transcripts** - `human_label` is the ground truth used to construct each
example, standing in for what a real reviewer would write after reading the
same two texts. Swap in a real, reviewer-labeled CSV with the same three
columns (`policy_snippet`, `agent_response`, `human_label`) and every script
below works identically - that substitution is the entire point of building
the pipeline against something you can already verify by eye.

## Run the comparison

```bash
python3 run_judge.py --judge v1 --judge v2
```

This is the actual, computed output from this repo's fixture judges against
`gold_labels.csv` - not a hypothetical:

```
=== judge_v1 ===
Accuracy:   73.9%
Cohen's kappa: 0.511 (moderate)
TPR (catches real hallucinations): 57.1%  [40/70]
FPR (flags real grounded answers):  0.0%  [0/45]

=== judge_v2 ===
Accuracy:   87.0%
Cohen's kappa: 0.742 (substantial)
TPR (catches real hallucinations): 78.6%  [55/70]
FPR (flags real grounded answers):  0.0%  [0/45]
```

## Why two judges

[`judges.py`](judges.py) has two heuristics, in the order you'd actually
write them:

- **`judge_v1`** - the judge you write in five minutes: flag a response as
  ungrounded if it contains a number that doesn't appear anywhere in the
  policy. It's precise (0% FPR - it never wrongly flags a real grounded
  answer) but catches only 57% of real hallucinations. Read the printed
  disagreements: it misses every case where the fabrication is a *scope*
  claim ("at any time," "no time limit," "automatically") rather than a
  fabricated number.
- **`judge_v2`** - `judge_v1` plus a check for unlicensed absolute phrasing.
  One calibration pass, driven by reading `judge_v1`'s actual misses against
  the gold set, raises kappa from 0.511 (moderate agreement - Landis &amp;
  Koch's convention, see [`metrics.py`](metrics.py)) to 0.742 (substantial)
  and TPR from 57% to 79% - **without any new false positives.** That's the
  calibration loop this whole stage is about: write a judge, run it against
  gold data, read what it actually got wrong, fix that specific gap, re-run.

**`judge_v2` still isn't perfect** - it still misses 3 cases, printed at the
end of its output. Two of them (`g066`, `g076`) reuse a number that's
present in the policy but attached to a *different* fact - shipping's
"2-3 business days" is the expedited timing, not standard's, but a plain
digit-presence check can't tell the difference. The third (`g021`) invents
an unstated condition ("as long as you return the original packaging")
using no number and no absolute-phrasing cue at all. Fixing those needs
actual semantic understanding of *which fact a number is attached to*, not
another keyword list - which is exactly why real judges are usually LLM
calls, not regexes, and why calibration doesn't stop after one pass. See
`judge_prompt_v2.txt` below for a rubric written to catch the "reused
number, wrong context" failure explicitly - the kind of fix an LLM judge can
make that a heuristic like `judge_v2` structurally can't.

## Why Cohen's kappa and not just accuracy

`judge_v1` scores 73.9% accuracy on a gold set that's 61% "grounded" - a
judge that said "grounded" for everything would score 61% by doing nothing.
Kappa corrects for that baseline: it measures agreement *beyond* what you'd
expect from each judge's own label distribution by chance. See
[`metrics.py`](metrics.py) for the from-scratch implementation (no
sklearn) - it's about 20 lines once you see the formula.

## `--live`: use a real model instead

```bash
python3 run_judge.py --judge v2 --live
```

Sends every row through [`judge_prompt_v2.txt`](judge_prompt_v2.txt) to a
real model via [`../common/llm_client.py`](../common/llm_client.py), instead
of the `judge_v2` heuristic. Requires `ANTHROPIC_API_KEY` or
`OPENAI_API_KEY`; 115 rows means 115 API calls, expect low-single-digit
dollars, not more. `judge_prompt_v1.txt` and `judge_prompt_v2.txt` are the
actual rubric text - `v2`'s rubric was written using the same misses that
motivated the `judge_v2` heuristic above, plus two worked examples, so you
can compare whether a real model's mistakes match, improve on, or differ
from the heuristic's. **They won't be identical** - that's expected and
worth sitting with, not a bug to fix.

## Try this

- Run `--judge v1 --judge v2 --live` back to back (edit `run_one_judge` to
  accept `--live` per-judge if you want both live) and compare a live
  model's misses against `judge_v2`'s three remaining misses above. Does it
  catch `g066`/`g076`, the reused-number-wrong-context cases?
- Write a `judge_v3` heuristic that also tracks *which fact* each number in
  the policy is attached to (e.g. split the snippet into clauses first),
  and see how much further kappa moves.
- Everything here is a binary judge. Real judges are often graded (1-5) -
  try converting `human_label` to a 3-point scale (`grounded`,
  `partially-grounded`, `ungrounded`) for the `g021`-style cases and see how
  much harder both the labeling and the kappa computation get.
