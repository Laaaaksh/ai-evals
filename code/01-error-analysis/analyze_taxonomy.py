#!/usr/bin/env python3
"""Turn a sheet of open-coded transcript labels into a failure-mode taxonomy
and a saturation curve - the two things error analysis is actually for.

Usage:
    python3 analyze_taxonomy.py reference_labels.csv
    python3 analyze_taxonomy.py my_labels.csv          # after you code transcripts.json yourself

This does no LLM calls and needs nothing beyond the standard library - the
work this script automates (reading transcripts and assigning a category) is
supposed to be done by a human first. Do that in transcripts.json before
running this on your own CSV; reference_labels.csv is provided so you can
check your own coding against it afterward, not as a shortcut past doing it.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter


def load_labels(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def taxonomy_table(rows: list[dict]) -> str:
    counts = Counter(r["failure_mode"] for r in rows)
    total = len(rows)
    lines = [f"{'failure_mode':<28}{'count':>7}{'share':>8}"]
    lines.append("-" * 43)
    for mode, n in counts.most_common():
        lines.append(f"{mode:<28}{n:>7}{n/total:>7.0%}")
    lines.append("-" * 43)
    lines.append(f"{'total transcripts':<28}{total:>7}")
    return "\n".join(lines)


def saturation_curve(rows: list[dict]) -> str:
    """At each transcript N, how many DISTINCT failure modes have been seen
    so far, in the order the transcripts were coded. This is the qualitative-
    research notion of saturation: once new transcripts stop introducing new
    categories, you likely have enough of the taxonomy to start building
    automated checks for it. A curve that's still climbing at the last row
    means: code more transcripts before you trust the taxonomy is complete.
    """
    seen: set[str] = set()
    lines = [f"{'n':>4}  {'new category?':<28}{'distinct so far':>16}"]
    lines.append("-" * 52)
    last_new_at = 0
    for i, r in enumerate(rows, start=1):
        mode = r["failure_mode"]
        is_new = mode not in seen
        seen.add(mode)
        if is_new:
            last_new_at = i
        marker = f"+ {mode}" if is_new else ""
        lines.append(f"{i:>4}  {marker:<28}{len(seen):>16}")
    lines.append("-" * 52)
    gap = len(rows) - last_new_at
    if gap >= 5:
        verdict = (
            f"No new category in the last {gap} transcripts - taxonomy looks "
            f"saturated at {len(seen)} categories."
        )
    else:
        verdict = (
            f"Last new category appeared only {gap} transcript(s) ago - code "
            f"more before trusting this taxonomy is complete."
        )
    lines.append(verdict)
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    rows = load_labels(sys.argv[1])
    if not rows:
        print("No rows found in", sys.argv[1])
        sys.exit(1)

    print(f"Failure-mode taxonomy from {sys.argv[1]} ({len(rows)} transcripts)\n")
    print(taxonomy_table(rows))
    print("\nSaturation curve (coding order = row order in the CSV)\n")
    print(saturation_curve(rows))


if __name__ == "__main__":
    main()
