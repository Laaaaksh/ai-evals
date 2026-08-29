"""Every case in regression_cases/ is a real (synthetic) production failure
that was diagnosed and fixed. This suite freezes each one as a test so it
can never silently resurface - the "data flywheel" idea: production
failures become permanent regression coverage, not one-off fixes.

Run:
    pytest test_regressions.py -v

This is the one sample in this repo wired into CI as an actual test run
(`.github/workflows/ci.yml`), not just a script that's executed once and
its output pasted into a README - a real pytest failure here blocks a PR,
the same way it would in a production repo.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from system_under_test import extract

CASES_DIR = Path(__file__).parent / "regression_cases"


def load_cases() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(CASES_DIR.glob("*.json"))]


CASES = load_cases()


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_regression_case(case: dict) -> None:
    actual = extract(case["input"])
    for field, expected_value in case["expected"].items():
        assert actual[field] == expected_value, (
            f"{case['id']}: expected {field}={expected_value!r}, got "
            f"{actual[field]!r}. This field was correct once - see "
            f"'why_this_case_exists' in {case['id']}.json for the original "
            f"bug this case protects against: {case['why_this_case_exists']}"
        )


def test_every_case_has_a_reason() -> None:
    """A regression case with no recorded reason is a regression case
    nobody can safely remove later - enforce the field exists and is
    non-trivial, not just present.
    """
    for case in CASES:
        assert len(case.get("why_this_case_exists", "")) > 20, (
            f"{case['id']} is missing a real 'why_this_case_exists' explanation"
        )
