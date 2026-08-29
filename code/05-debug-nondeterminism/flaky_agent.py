"""A simulated agent that fails for four different, specific reasons - the
same four buckets a real intermittent-failure investigation has to tell
apart:

- prompt_sensitivity: a wording variant of the exact same request confuses
  the agent.
- retrieval_variance: the retrieval step occasionally returns a stale
  document instead of the current one.
- tool_format: the tool call is occasionally malformed.
- judge_noise: the agent's answer was actually correct, but the grading
  step itself flips it to a fail.

Nothing here calls a real model - it's a controlled simulation with a known
ground truth (`true_cause`), specifically so diagnose.py's diagnosis can be
checked against a real answer afterward, the same way Stage 1's
`analyze_taxonomy.py` checks a reader's own coding against
`reference_labels.csv`. Every run is a pure function of a seeded
`random.Random` instance - no global random state, no wall-clock
dependency, so the whole 200-trial run in diagnose.py is exactly
reproducible.
"""
from __future__ import annotations

import random

PROMPT_VARIANTS = ["v1", "v2", "v3"]
# v1: "Where's my order {order_id}?"
# v2: "Can you check on {order_id}?"        <- ambiguous enough to sometimes
#                                               read as a cancellation-adjacent
#                                               request instead of a status one
# v3: "Status of {order_id} please"

RETRIEVAL_STALE_RATE = 0.15   # retrieval returns a stale snapshot doc
TOOL_MALFORMED_RATE = 0.10    # tool call comes back malformed
PROMPT_V2_CONFUSION_RATE = 0.60  # of v2 runs specifically, how often it confuses the agent
JUDGE_NOISE_RATE = 0.08       # of CORRECT answers, how often the judge wrongly fails them


def run_once(rng: random.Random) -> dict:
    prompt_variant = rng.choice(PROMPT_VARIANTS)
    prompt_confuses_agent = prompt_variant == "v2" and rng.random() < PROMPT_V2_CONFUSION_RATE

    retrieved_doc = "stale" if rng.random() < RETRIEVAL_STALE_RATE else "current"
    tool_call_malformed = rng.random() < TOOL_MALFORMED_RATE

    if tool_call_malformed:
        answer_correct, cause = False, "tool_format"
    elif retrieved_doc == "stale":
        answer_correct, cause = False, "retrieval_variance"
    elif prompt_confuses_agent:
        answer_correct, cause = False, "prompt_sensitivity"
    else:
        answer_correct, cause = True, None

    graded_pass = answer_correct
    if answer_correct and rng.random() < JUDGE_NOISE_RATE:
        graded_pass = False
        cause = "judge_noise"

    return {
        "prompt_variant": prompt_variant,
        "retrieved_doc": retrieved_doc,
        "tool_call_malformed": tool_call_malformed,
        "graded_pass": graded_pass,
        "true_cause": None if graded_pass else cause,
    }


def run_many(n: int, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    return [run_once(rng) for _ in range(n)]
