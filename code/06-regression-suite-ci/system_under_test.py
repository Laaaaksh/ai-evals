"""A small, rule-based (not LLM-based) version of the same extraction task
from Stage 2 - order_id, intent, sentiment from a support message. Rule-
based on purpose: it's simple enough that you can point at the exact line
that caused each historical bug in `regression_cases/`, and simple enough to
break again if you edit it carelessly - which is exactly what "Try this"
below asks you to do.

This is the CURRENT, FIXED version. Every case in regression_cases/ records
a real (synthetic) production failure this code used to have, what the
buggy output looked like, and what it must produce instead - permanently,
enforced by test_regressions.py.
"""
from __future__ import annotations

import re

ORDER_ID_RE = re.compile(r"\b([A-Za-z]\d{4}|\d{2,})\b")

CANCEL_WORDS = ["cancel"]
REFUND_WORDS = ["refund", "money back", "reimburse"]
NEGATIONS = ["not", "n't", "don't", "wasn't", "isn't"]
FRUSTRATION_WORDS = ["annoyed", "upset", "frustrated", "annoying"]
ANGER_WORDS = ["furious", "ridiculous", "unacceptable", "angry"]


def extract_order_id(message: str) -> str | None:
    match = ORDER_ID_RE.search(message)
    if not match:
        return None
    return match.group(1).upper()


def extract_intent(message: str) -> str:
    lower = message.lower()
    if any(w in lower for w in CANCEL_WORDS):
        return "cancel"
    if any(w in lower for w in REFUND_WORDS):
        return "refund"
    if "status" in lower or "where" in lower or "check" in lower or "wondering" in lower:
        return "status"
    return "other"


def extract_sentiment(message: str) -> str:
    lower = message.lower()
    words = lower.split()

    def negated_near(trigger: str) -> bool:
        """A trigger word is negated if a negation word appears within the
        3 words before it - "not upset" or "not really annoyed" should not
        count as frustration.
        """
        if trigger not in lower:
            return False
        idx = next((i for i, w in enumerate(words) if trigger in w), None)
        if idx is None:
            return False
        window = words[max(0, idx - 3):idx]
        return any(any(neg in w for neg in NEGATIONS) for w in window)

    if any(w in lower for w in ANGER_WORDS):
        return "angry"
    for w in FRUSTRATION_WORDS:
        if w in lower and not negated_near(w):
            return "frustrated"
    return "neutral"


def extract(message: str) -> dict:
    return {
        "order_id": extract_order_id(message),
        "intent": extract_intent(message),
        "sentiment": extract_sentiment(message),
    }
