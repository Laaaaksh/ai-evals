"""Agreement metrics for judge calibration, implemented from scratch (no
sklearn/numpy dependency) so the arithmetic is visible, not a library call.

These are the metrics that matter when validating an LLM judge against a
human-labeled gold set:

- Raw accuracy overstates agreement on imbalanced data (a judge that always
  says "grounded" scores high accuracy if most examples really are grounded).
- Cohen's kappa corrects for the agreement you'd expect by chance alone -
  it's the standard metric in inter-rater reliability research for exactly
  this reason.
- TPR/FPR (and precision/recall) tell you WHICH kind of mistake the judge
  makes: TPR is "of the real hallucinations, how many did the judge catch,"
  FPR is "of the real grounded responses, how often did the judge cry wolf."
  Cohen's kappa alone can't distinguish those - a full calibration writeup
  needs both.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConfusionMatrix:
    tp: int  # predicted positive, actually positive
    fp: int  # predicted positive, actually negative
    tn: int  # predicted negative, actually negative
    fn: int  # predicted negative, actually positive

    @property
    def n(self) -> int:
        return self.tp + self.fp + self.tn + self.fn

    @property
    def accuracy(self) -> float:
        return (self.tp + self.tn) / self.n if self.n else 0.0

    @property
    def tpr(self) -> float:
        """True positive rate / recall / sensitivity."""
        denom = self.tp + self.fn
        return self.tp / denom if denom else 0.0

    @property
    def fpr(self) -> float:
        """False positive rate."""
        denom = self.fp + self.tn
        return self.fp / denom if denom else 0.0

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return self.tp / denom if denom else 0.0


def confusion_matrix(predicted: list[str], actual: list[str], positive_label: str) -> ConfusionMatrix:
    if len(predicted) != len(actual):
        raise ValueError("predicted and actual must be the same length")
    tp = fp = tn = fn = 0
    for p, a in zip(predicted, actual):
        p_pos = p == positive_label
        a_pos = a == positive_label
        if p_pos and a_pos:
            tp += 1
        elif p_pos and not a_pos:
            fp += 1
        elif not p_pos and a_pos:
            fn += 1
        else:
            tn += 1
    return ConfusionMatrix(tp=tp, fp=fp, tn=tn, fn=fn)


def cohens_kappa(rater_a: list[str], rater_b: list[str]) -> float:
    """Cohen's kappa between two raters over the same items, for any number
    of label categories (not just binary). kappa = (po - pe) / (1 - pe)
    where po is observed agreement and pe is agreement expected by chance,
    given each rater's own marginal label distribution.
    """
    if len(rater_a) != len(rater_b):
        raise ValueError("rater_a and rater_b must be the same length")
    n = len(rater_a)
    if n == 0:
        return 0.0

    labels = sorted(set(rater_a) | set(rater_b))

    po = sum(1 for a, b in zip(rater_a, rater_b) if a == b) / n

    a_counts = {label: rater_a.count(label) for label in labels}
    b_counts = {label: rater_b.count(label) for label in labels}
    pe = sum((a_counts[l] / n) * (b_counts[l] / n) for l in labels)

    if pe == 1.0:
        return 1.0  # both raters unanimous on the same single label
    return (po - pe) / (1 - pe)


KAPPA_INTERPRETATION = [
    (0.81, "almost perfect"),
    (0.61, "substantial"),
    (0.41, "moderate"),
    (0.21, "fair"),
    (0.01, "slight"),
    (float("-inf"), "poor / no better than chance"),
]


def interpret_kappa(kappa: float) -> str:
    """Landis & Koch (1977) benchmark bands - a convention, not a law of
    nature, but the one most eval-calibration writeups cite. See
    resources/curated-resources.md for the sources behind this file's
    approach to judge calibration.
    """
    for threshold, label in KAPPA_INTERPRETATION:
        if kappa >= threshold:
            return label
    return "poor / no better than chance"
