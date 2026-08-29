#!/usr/bin/env python3
"""Run a judge over gold_labels.csv and report agreement with human_label:
accuracy, Cohen's kappa, TPR/FPR, precision, and a confusion matrix - then
list every disagreement so you can read the actual misses, not just the
number.

Usage:
    python3 run_judge.py --judge v1
    python3 run_judge.py --judge v2
    python3 run_judge.py --judge v1 --judge v2     # compare both, side by side
    python3 run_judge.py --judge v2 --live         # call a real model with judge_prompt_v2.txt

--live requires ANTHROPIC_API_KEY or OPENAI_API_KEY and makes one API call
per row (115 rows in the provided gold set) - expect it to cost low single
digit dollars, not more. Without --live, judge_v1/judge_v2 are pure
functions with no network call.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from llm_client import NoAPIKeyError  # noqa: E402
from judges import JUDGES, llm_judge  # noqa: E402
from metrics import cohens_kappa, confusion_matrix, interpret_kappa  # noqa: E402


def load_gold(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_one_judge(name: str, rows: list[dict], live: bool) -> None:
    predictions = []
    for row in rows:
        if live:
            prompt_path = f"judge_prompt_{name}.txt"
            pred = llm_judge(row["policy_snippet"], row["agent_response"], prompt_path)
        else:
            if name not in JUDGES:
                raise SystemExit(
                    f"No offline heuristic for judge {name!r} - only v1 and v2 have "
                    f"one. Add --live to call a real model with judge_prompt_{name}.txt."
                )
            pred = JUDGES[name](row["policy_snippet"], row["agent_response"])
        predictions.append(pred)

    actual = [row["human_label"] for row in rows]
    cm = confusion_matrix(predictions, actual, positive_label="ungrounded")
    kappa = cohens_kappa(predictions, actual)

    print(f"=== judge_{name}{' (live)' if live else ''} ===")
    print(f"Accuracy:   {cm.accuracy:.1%}")
    print(f"Cohen's kappa: {kappa:.3f} ({interpret_kappa(kappa)})")
    print(f"TPR (catches real hallucinations): {cm.tpr:.1%}  [{cm.tp}/{cm.tp + cm.fn}]")
    print(f"FPR (flags real grounded answers):  {cm.fpr:.1%}  [{cm.fp}/{cm.fp + cm.tn}]")
    print(f"Precision:  {cm.precision:.1%}")
    print(f"Confusion matrix (positive class = ungrounded):")
    print(f"                 actual ungrounded   actual grounded")
    print(f"  pred ungrounded  {cm.tp:>15}   {cm.fp:>15}")
    print(f"  pred grounded    {cm.fn:>15}   {cm.tn:>15}")

    misses = [
        (row, pred)
        for row, pred in zip(rows, predictions)
        if pred != row["human_label"]
    ]
    print(f"\n{len(misses)} disagreement(s) with human_label:")
    seen_responses: set[str] = set()
    shown = 0
    for row, pred in misses:
        # gold_labels.csv repeats each core claim under 5 phrasing wrappers;
        # show one example per distinct underlying miss, not all 5.
        key = row["human_label"] + row["agent_response"][-40:]
        if key in seen_responses:
            continue
        seen_responses.add(key)
        shown += 1
        print(f"  [{row['id']}] judge said {pred!r}, human said {row['human_label']!r}")
        print(f"    response: {row['agent_response']!r}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--judge", action="append", required=True, choices=["v1", "v2"],
                         help="Repeat to compare multiple judge versions in one run")
    parser.add_argument("--gold", default="gold_labels.csv")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    rows = load_gold(args.gold)
    try:
        for name in args.judge:
            run_one_judge(name, rows, args.live)
    except NoAPIKeyError as e:
        raise SystemExit(f"error: {e}")


if __name__ == "__main__":
    main()
