#!/usr/bin/env python3
"""Run every check registered in eval_suite.py over a set of cases, print a
pass/fail grid, and exit non-zero if the aggregate pass rate drops below a
threshold - the property that makes an eval suite usable as a CI gate later
(Stage 6 builds on exactly this exit-code contract).

Usage:
    python3 run_eval.py cases.jsonl fixture_outputs.jsonl
    python3 run_eval.py cases.jsonl fixture_outputs.jsonl --fail-under 0.9
    python3 run_eval.py cases.jsonl --live      # call a real model instead of fixtures

--live requires ANTHROPIC_API_KEY or OPENAI_API_KEY - see ../common/llm_client.py.
Without --live, no network call is made and no API key is needed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eval_suite import all_checks

EXTRACTION_PROMPT = """Extract three fields from the support message below and
respond with ONLY a JSON object, no other text: order_id (string), intent
(one of: status, refund, cancel, other), sentiment (one of: neutral,
frustrated, angry).

Message: {message}"""


def load_jsonl(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def get_outputs_live(cases: list[dict]) -> dict[str, str]:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
    import llm_client

    outputs = {}
    for case in cases:
        prompt = EXTRACTION_PROMPT.format(message=case["input"])
        outputs[case["id"]] = llm_client.complete(prompt)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases_path")
    parser.add_argument("outputs_path", nargs="?", default="fixture_outputs.jsonl")
    parser.add_argument("--fail-under", type=float, default=0.0)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    cases = load_jsonl(args.cases_path)

    if args.live:
        outputs_by_id = get_outputs_live(cases)
    else:
        outputs = load_jsonl(args.outputs_path)
        outputs_by_id = {o["id"]: o["output"] for o in outputs}

    checks = all_checks()
    check_names = list(checks)

    header = f"{'id':<5}" + "".join(f"{name:<20}" for name in check_names)
    print(header)
    print("-" * len(header))

    total_checks = 0
    passed_checks = 0
    failures: list[str] = []

    for case in cases:
        output = outputs_by_id.get(case["id"], "")
        row = f"{case['id']:<5}"
        for name in check_names:
            result = checks[name](case, output)
            total_checks += 1
            if result.passed:
                passed_checks += 1
                row += f"{'PASS':<20}"
            else:
                row += f"{'FAIL':<20}"
                failures.append(f"  {case['id']} / {name}: {result.message}")
        print(row)

    pass_rate = passed_checks / total_checks if total_checks else 0.0
    print("-" * len(header))
    print(f"{passed_checks}/{total_checks} checks passed ({pass_rate:.0%})\n")

    if failures:
        print("Failures:")
        print("\n".join(failures))
        print()

    if pass_rate < args.fail_under:
        print(f"FAIL: pass rate {pass_rate:.0%} is below --fail-under {args.fail_under:.0%}")
        sys.exit(1)
    print("OK" if args.fail_under else "Done (no --fail-under threshold set, so this always exits 0)")


if __name__ == "__main__":
    main()
