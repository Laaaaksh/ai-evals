"""Three judge implementations for the grounding task, in increasing order
of sophistication:

- judge_v1: a naive heuristic - flags a response as ungrounded only if it
  contains a number that doesn't appear anywhere in the policy snippet.
  Stands in for "the first judge you write," which usually pattern-matches
  on the most obvious signal and misses everything else.
- judge_v2: judge_v1 plus a check for unconditional/absolute phrasing
  ("at any time," "automatically," "no problem") that isn't licensed by the
  snippet. Stands in for "the judge after one calibration pass against gold
  data" - it catches a real category v1 missed, without becoming perfect.
- llm_judge: an actual LLM call using judge_prompt_v1.txt / v2.txt, for
  --live mode. Uses the SAME prompt text a human would read, so the
  fixture/live modes are teaching the same rubric two different ways.

judge_v1 and judge_v2 are intentionally simple and imperfect - real judge
calibration means finding and fixing exactly this kind of gap, not writing
a judge that's already perfect on the first try. See README.md for the
specific cases both versions still miss.
"""
from __future__ import annotations

import re

SCOPE_CUES = [
    "at any time", "any order", "no time limit", "no limit",
    "even after", "automatically", "no problem", "immediately",
]


def _numbers(text: str) -> set[str]:
    return set(re.findall(r"\d+", text))


def judge_v1(snippet: str, response: str) -> str:
    new_numbers = _numbers(response) - _numbers(snippet)
    return "ungrounded" if new_numbers else "grounded"


def judge_v2(snippet: str, response: str) -> str:
    new_numbers = _numbers(response) - _numbers(snippet)
    if new_numbers:
        return "ungrounded"
    response_lower = response.lower()
    for cue in SCOPE_CUES:
        if cue in response_lower and cue not in snippet.lower():
            return "ungrounded"
    return "grounded"


def llm_judge(snippet: str, response: str, prompt_path: str) -> str:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
    import llm_client

    with open(prompt_path, encoding="utf-8") as f:
        template = f.read()
    prompt = template.format(snippet=snippet, response=response)
    raw = llm_client.complete(prompt).strip().lower()
    return "ungrounded" if "ungrounded" in raw else "grounded"


JUDGES = {"v1": judge_v1, "v2": judge_v2}
