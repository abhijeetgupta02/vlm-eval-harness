"""Simple, transparent metrics.

Only exact-match accuracy is implemented. Every number here is computed from
actual model outputs -- nothing is hard-coded or assumed.
"""

from __future__ import annotations

from dataclasses import dataclass


def normalize(text: str) -> str:
    """Normalize an answer for exact-match comparison.

    Lowercases, strips surrounding whitespace, and strips a few trailing
    punctuation marks. Deliberately conservative -- it does not try to be a
    smart answer matcher.
    """
    return text.strip().lower().rstrip(".!?")


def exact_match(predicted: str, expected: str) -> bool:
    """Return True iff ``predicted`` matches ``expected`` after normalization."""
    return normalize(predicted) == normalize(expected)


@dataclass(frozen=True)
class Metrics:
    """Aggregated metrics for a run."""

    num_examples: int
    num_correct: int

    @property
    def accuracy(self) -> float:
        """Fraction correct in [0, 1]; 0.0 when there are no examples."""
        if self.num_examples == 0:
            return 0.0
        return self.num_correct / self.num_examples

    def as_dict(self) -> dict[str, float | int]:
        return {
            "num_examples": self.num_examples,
            "num_correct": self.num_correct,
            "accuracy": self.accuracy,
        }


def aggregate(correct_flags: list[bool]) -> Metrics:
    """Aggregate a list of per-example correctness flags into :class:`Metrics`."""
    return Metrics(
        num_examples=len(correct_flags),
        num_correct=sum(1 for flag in correct_flags if flag),
    )
