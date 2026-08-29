# 01 — Error analysis

24 synthetic transcripts of a customer-support agent (order status, refunds,
cancellations) in [`transcripts.json`](transcripts.json). No labels attached.
Your job, before running anything: **read every transcript and assign each
one a failure-mode category in your own words** - a spreadsheet, a text file,
whatever. This is open coding: you don't start with a taxonomy, you build one
by noticing what's actually wrong, transcript by transcript, and merging
similar problems into the same label as you go.

Companion to [`curriculum/01-error-analysis.md`](../../curriculum/01-error-analysis.md).

## Do this first, by hand

1. Read `transcripts.json`. For each transcript, decide: did the agent get
   this right? If not, what specifically went wrong - in a few words, not a
   full sentence.
2. As you go, reuse a label if you've seen the same problem before instead of
   inventing a new one each time. That's the whole exercise: forcing
   yourself to notice when two failures are "the same kind of wrong."
3. Save your labels as a CSV with a header `id,failure_mode,notes` - one row
   per transcript.

Don't skip to the reference answer key first. The value here is in the
noticing, not in matching a key.

## Then run this

```bash
python3 analyze_taxonomy.py your_labels.csv
```

This prints two things, computed from nothing but your CSV:

- A **frequency table** - which failure modes are most common, so you know
  where fixing the agent would matter most.
- A **saturation curve** - at each transcript, how many distinct categories
  you'd found so far, in the order you coded them. If the curve is still
  climbing in your last few transcripts, you haven't seen enough examples yet
  to trust that your taxonomy is complete. This is a real technique from
  qualitative research (grounded theory's "theoretical saturation"), not
  something specific to LLM evals - it's just rarely applied to transcripts.

## Compare against the reference coding

```bash
python3 analyze_taxonomy.py reference_labels.csv
```

[`reference_labels.csv`](reference_labels.csv) is one reasonable coding of
the same 24 transcripts, with a `notes` column explaining each call. It finds
7 categories: `ok`, `hallucinated_policy`, `tool_arg_formatting`,
`ignored_user_constraint`, `redundant_tool_calls`, `incomplete_answer`, and
`unnecessary_refusal`. Yours doesn't need to match exactly - category
*names* are arbitrary. What matters is whether you noticed the same
underlying problems and grouped them consistently. If you invented 15
categories for 24 transcripts, you were probably splitting the same failure
into too many buckets; if you found only 2, you were probably lumping
different failures together.

Where your coding disagrees with the reference, go back to that specific
transcript and ask why - that disagreement is the useful part, not an error
to shrug off.

## What to look for in the transcripts

Without spoiling every case: some agents here ignore an explicit user
instruction, some assert a policy that was never grounded in a tool call,
some call the same tool repeatedly with no new information, and some answer
only half of a two-part question. None of these would be caught by a naive
"did the agent produce a response" check - that's the point of doing this
before Stage 2 builds automated checks.

## Notes on the fixture data

`transcripts.json` is synthetic, written for this repo - not real production
data. Real error analysis is done on your own system's real transcripts;
this sample exists so you can practice the *method* (open coding → taxonomy
→ saturation check) on something small and self-contained before doing it
for real. `analyze_taxonomy.py` has no dependencies beyond the Python
standard library and makes no network calls.
