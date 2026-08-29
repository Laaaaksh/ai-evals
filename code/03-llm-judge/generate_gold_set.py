#!/usr/bin/env python3
"""Build gold_labels.csv: a synthetic gold set for a "grounding" judge task -
given a policy snippet and an agent's response to a policy question, is the
response GROUNDED (only asserts facts present in the snippet) or UNGROUNDED
(asserts a fabricated number, condition, or scope not in the snippet)?

This is a real, common judge task - it's the core check behind most RAG
"faithfulness"/"hallucination" evals. The data here is synthetic and
template-generated, not scraped real transcripts: `human_label` is the
ground truth used to CONSTRUCT each example, standing in for what a real
human annotator would have written after reading the same two texts. That's
a deliberate simplification so this sample's metrics are computed against
real, verifiable signal without needing an actual labeling pass - swap in a
real reviewer-labeled CSV with the same three columns and every script past
this one works identically.

Deterministic - same output every run, no randomness, no network. Run it
yourself to regenerate gold_labels.csv:

    python3 generate_gold_set.py > gold_labels.csv
"""
from __future__ import annotations

import csv
import sys

# (snippet_id, policy_snippet, [(response, human_label), ...])
TEMPLATES: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "damaged_item",
        "Damaged items may be replaced free of charge within 45 days of "
        "purchase. Cash refunds are not offered for damaged items; store "
        "credit is issued instead.",
        [
            ("Since it arrived damaged, we'll replace it for free - no cost "
             "to you, as long as it's within 45 days of your purchase.", "grounded"),
            ("We can't issue a cash refund for a damaged item, but we'll "
             "give you store credit instead.", "grounded"),
            ("We'll issue a full cash refund for the damaged item within "
             "24 hours.", "ungrounded"),
            ("Damaged items can be replaced free of charge at any time, "
             "no time limit.", "ungrounded"),
            ("We'll replace it for free within 45 days, as long as you "
             "return the original packaging.", "ungrounded"),
            ("You have 90 days to request a free replacement for damaged "
             "items.", "ungrounded"),
        ],
    ),
    (
        "cancellation",
        "Orders can be cancelled any time before they ship. Once an order "
        "has shipped, it cannot be cancelled, but a return can be requested "
        "after delivery.",
        [
            ("Since your order hasn't shipped yet, I can cancel it right "
             "now.", "grounded"),
            ("It's already shipped, so I can't cancel it, but you can "
             "return it once it arrives.", "grounded"),
            ("I can cancel it even though it's already shipped, "
             "automatically, no problem.", "ungrounded"),
            ("You have 30 days after shipping to cancel.", "ungrounded"),
            ("I can cancel any order at any time, even after delivery.", "ungrounded"),
        ],
    ),
    (
        "shipping_speed",
        "Standard shipping takes 5-7 business days at no extra cost. "
        "Expedited shipping is available for an additional $12 and takes "
        "2-3 business days.",
        [
            ("Standard shipping is free and takes 5 to 7 business days.", "grounded"),
            ("If you need it faster, expedited shipping is $12 extra and "
             "takes 2-3 business days.", "grounded"),
            ("Standard shipping is free and arrives in 2-3 business days.", "ungrounded"),
            ("Expedited shipping is free if your order is over $50.", "ungrounded"),
            ("Standard shipping takes 5-7 business days and costs $5.", "ungrounded"),
        ],
    ),
    (
        "price_match",
        "We do not price match other retailers.",
        [
            ("We don't price match other retailers, sorry about that.", "grounded"),
            ("Yes, we automatically price match and refund the difference "
             "within 24 hours.", "ungrounded"),
            ("We price match, but only for orders placed in the last 7 "
             "days.", "ungrounded"),
        ],
    ),
    (
        "referral",
        "Referral program: the referrer receives a $10 account credit "
        "after the referred friend completes their first order. No "
        "discount is applied automatically at checkout for either party.",
        [
            ("Your friend needs to complete their first order before you "
             "get a $10 credit - it's not automatic at checkout.", "grounded"),
            ("The referral credit is $10 store credit after your friend's "
             "first completed order.", "grounded"),
            ("You get 25% off your next order and your friend gets 15% "
             "off, applied automatically at checkout.", "ungrounded"),
            ("The referral credit is $20, applied immediately when you "
             "send the invite.", "ungrounded"),
        ],
    ),
]

WRAPPERS = [
    "{claim}",
    "Thanks for reaching out! {claim}",
    "Sure, happy to help. {claim}",
    "Got it. {claim}",
    "I checked your order. {claim}",
]


def main() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["id", "policy_snippet", "agent_response", "human_label"])
    i = 0
    for snippet_id, snippet, examples in TEMPLATES:
        for claim, label in examples:
            for wrapper in WRAPPERS:
                i += 1
                response = wrapper.format(claim=claim)
                writer.writerow([f"g{i:03d}", snippet, response, label])


if __name__ == "__main__":
    main()
