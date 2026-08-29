#!/usr/bin/env python3
"""Diagnose why a flaky agent fails, using only observable run data - the
same input run N times, with each run's prompt variant, retrieved doc, and
tool-call validity logged - not the ground-truth cause. That's the real
constraint when debugging a flaky production agent: you can see what varied
between runs, but nothing tells you up front which variation caused which
failure.

Method: for each observable factor, compare the failure rate when that
factor takes a given value against the overall baseline failure rate. A
factor value with a much higher failure rate than baseline is a real
suspect; failures that remain after accounting for every suspect factor are
"unexplained" - and an unexplained cluster is itself a diagnosis: it points
at something that isn't a property of the input at all (grading noise, a
race condition, infra flakiness), because if it were input-driven, some
observable input factor would correlate with it.

Usage:
    python3 diagnose.py                    # diagnosis only
    python3 diagnose.py --reveal           # diagnosis, then check it against ground truth
    python3 diagnose.py --trials 500       # more trials = more stable failure-rate estimates
"""
from __future__ import annotations

import argparse
from collections import Counter

from flaky_agent import run_many

LIFT_THRESHOLD = 2.0  # flag a factor value as a suspect if its failure rate is >= 2x baseline


def failure_rate(runs: list[dict]) -> float:
    if not runs:
        return 0.0
    return sum(1 for r in runs if not r["graded_pass"]) / len(runs)


def factor_breakdown(runs: list[dict], factor: str, baseline: float) -> list[tuple]:
    values = sorted({r[factor] for r in runs}, key=str)
    rows = []
    for value in values:
        subset = [r for r in runs if r[factor] == value]
        rate = failure_rate(subset)
        lift = rate / baseline if baseline else 0.0
        rows.append((value, len(subset), rate, lift))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--reveal", action="store_true", help="show ground-truth true_cause counts for comparison")
    args = parser.parse_args()

    runs = run_many(args.trials, seed=args.seed)
    baseline = failure_rate(runs)
    n_fail = sum(1 for r in runs if not r["graded_pass"])

    print(f"{args.trials} runs of the same input, same seed policy - {n_fail} failed ({baseline:.1%})\n")

    factors = ["prompt_variant", "retrieved_doc", "tool_call_malformed"]
    suspects: dict[str, set] = {}

    for factor in factors:
        print(f"By {factor}:")
        rows = factor_breakdown(runs, factor, baseline)
        for value, count, rate, lift in rows:
            flag = f"  <- {lift:.1f}x baseline, SUSPECT" if lift >= LIFT_THRESHOLD else ""
            print(f"  {value!s:<10} n={count:<4} fail_rate={rate:.1%}{flag}")
            if lift >= LIFT_THRESHOLD:
                suspects.setdefault(factor, set()).add(value)
        print()

    def explained(run: dict) -> bool:
        return any(
            factor in suspects and run[factor] in suspects[factor]
            for factor in factors
        )

    failing = [r for r in runs if not r["graded_pass"]]
    unexplained = [r for r in failing if not explained(r)]

    print(f"Suspect factor values: {suspects or 'none'}")
    print(
        f"{len(failing) - len(unexplained)}/{len(failing)} failures explained by a "
        f"suspect input factor."
    )
    print(
        f"{len(unexplained)}/{len(failing)} failures are NOT explained by any input "
        f"factor tested - none of prompt wording, retrieved doc, or tool-call "
        f"validity differs between these failing runs and the passing ones.\n"
        f"That residual is itself the diagnosis: since it doesn't correlate with "
        f"anything about the input, the next place to look is the grading/judging "
        f"step, not the agent - see Stage 3 (LLM-as-judge) for how a judge's own "
        f"noise gets measured, not just assumed."
    )

    if args.reveal:
        print("\n--- ground truth (for checking the diagnosis above) ---")
        causes = Counter(r["true_cause"] for r in runs if r["true_cause"])
        for cause, count in causes.most_common():
            print(f"  {cause:<20} {count:>4} ({count / args.trials:.1%} of all runs)")


if __name__ == "__main__":
    main()
