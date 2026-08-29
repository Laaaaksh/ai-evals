"""A minimal eval framework: register checks, run them over (case, output)
pairs, get back a score. This is deliberately small - real frameworks
(promptfoo, DeepEval - see resources/curated-resources.md) do much more, but
the core idea is exactly this: a check is a pure function from
(expected, actual) to a pass/fail plus a reason, and an eval suite is just a
list of them applied consistently.

The task under test: extract structured fields from a support message -
order_id, intent, and sentiment - as JSON. This is representative of a huge
share of real agent evals: not "is the prose good" but "did the structured
output have the right shape and the right values."
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

VALID_INTENTS = {"status", "refund", "cancel", "other"}
VALID_SENTIMENTS = {"neutral", "frustrated", "angry"}
REQUIRED_FIELDS = {"order_id", "intent", "sentiment"}


@dataclass
class CheckResult:
    passed: bool
    message: str


Check = Callable[[dict, str], CheckResult]
_REGISTRY: dict[str, Check] = {}


def check(name: str):
    """Decorator: register a function as a named check in the suite."""

    def wrap(fn: Check) -> Check:
        _REGISTRY[name] = fn
        return fn

    return wrap


def all_checks() -> dict[str, Check]:
    return dict(_REGISTRY)


def _try_parse(output: str) -> dict | None:
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


@check("valid_json")
def valid_json(case: dict, output: str) -> CheckResult:
    parsed = _try_parse(output)
    if parsed is None:
        return CheckResult(False, "output is not valid JSON (or not a JSON object)")
    return CheckResult(True, "parses as a JSON object")


@check("has_required_fields")
def has_required_fields(case: dict, output: str) -> CheckResult:
    parsed = _try_parse(output)
    if parsed is None:
        return CheckResult(False, "skipped - not valid JSON")
    missing = REQUIRED_FIELDS - parsed.keys()
    if missing:
        return CheckResult(False, f"missing fields: {sorted(missing)}")
    return CheckResult(True, "all required fields present")


@check("intent_in_enum")
def intent_in_enum(case: dict, output: str) -> CheckResult:
    parsed = _try_parse(output)
    if parsed is None or "intent" not in parsed:
        return CheckResult(False, "skipped - no intent field to check")
    if parsed["intent"] not in VALID_INTENTS:
        return CheckResult(
            False, f"intent {parsed['intent']!r} not in {sorted(VALID_INTENTS)}"
        )
    return CheckResult(True, "intent is a valid enum value")


@check("sentiment_in_enum")
def sentiment_in_enum(case: dict, output: str) -> CheckResult:
    parsed = _try_parse(output)
    if parsed is None or "sentiment" not in parsed:
        return CheckResult(False, "skipped - no sentiment field to check")
    if parsed["sentiment"] not in VALID_SENTIMENTS:
        return CheckResult(
            False, f"sentiment {parsed['sentiment']!r} not in {sorted(VALID_SENTIMENTS)}"
        )
    return CheckResult(True, "sentiment is a valid enum value")


@check("order_id_correct")
def order_id_correct(case: dict, output: str) -> CheckResult:
    parsed = _try_parse(output)
    expected = case["expected"]["order_id"]
    if parsed is None or "order_id" not in parsed:
        return CheckResult(False, "skipped - no order_id field to check")
    if parsed["order_id"] != expected:
        return CheckResult(False, f"got {parsed['order_id']!r}, expected {expected!r}")
    return CheckResult(True, "order_id matches exactly")


@check("intent_correct")
def intent_correct(case: dict, output: str) -> CheckResult:
    parsed = _try_parse(output)
    expected = case["expected"]["intent"]
    if parsed is None or "intent" not in parsed:
        return CheckResult(False, "skipped - no intent field to check")
    if parsed["intent"] != expected:
        return CheckResult(False, f"got {parsed['intent']!r}, expected {expected!r}")
    return CheckResult(True, "intent matches expected")


@check("sentiment_correct")
def sentiment_correct(case: dict, output: str) -> CheckResult:
    """Graded, not exact: sentiment is inherently a judgment call, so
    adjacent categories (neutral vs. frustrated) are treated as a partial
    miss worth flagging differently from a hard miss (neutral vs. angry).
    This is the smallest possible taste of "graded" vs. "binary" checks -
    Stage 3 goes further with an actual LLM judge for genuinely subjective
    calls this kind of hand-written rule can't make well.
    """
    parsed = _try_parse(output)
    expected = case["expected"]["sentiment"]
    if parsed is None or "sentiment" not in parsed:
        return CheckResult(False, "skipped - no sentiment field to check")
    got = parsed["sentiment"]
    if got == expected:
        return CheckResult(True, "sentiment matches expected exactly")
    adjacent = {
        ("neutral", "frustrated"), ("frustrated", "neutral"),
        ("frustrated", "angry"), ("angry", "frustrated"),
    }
    if (got, expected) in adjacent:
        return CheckResult(False, f"got {got!r}, expected {expected!r} (adjacent, not exact)")
    return CheckResult(False, f"got {got!r}, expected {expected!r} (not adjacent)")
