"""A tiny in-repo toy benchmark.

This is NOT a real published benchmark. It is a handful of hard-coded
question/answer pairs whose only purpose is to exercise the pipeline. The data
is structured so an ``image`` path could be plugged in later, but for now the
``image`` field holds a placeholder id and the task is text-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Example:
    """A single benchmark item."""

    id: str
    question: str
    expected_answer: str
    # Placeholder for a future image path; None means "text-only for now".
    image: str | None = None

    def to_model_input(self) -> dict[str, Any]:
        """Render this example as a model-adapter input dict."""
        return {"id": self.id, "question": self.question, "image": self.image}


# Hard-coded toy data. Answers are short, lowercase, exact-match targets.
_EXAMPLES: list[Example] = [
    Example(
        id="toy-001",
        question="What is 2 + 2?",
        expected_answer="4",
        image="placeholder://toy-001",
    ),
    Example(
        id="toy-002",
        question="What color is a clear daytime sky?",
        expected_answer="blue",
        image="placeholder://toy-002",
    ),
    Example(
        id="toy-003",
        question="How many legs does a spider have?",
        expected_answer="8",
        image="placeholder://toy-003",
    ),
    Example(
        id="toy-004",
        question="What is the capital of France?",
        expected_answer="paris",
        image="placeholder://toy-004",
    ),
    Example(
        id="toy-005",
        question="What is the opposite of 'hot'?",
        expected_answer="cold",
        image="placeholder://toy-005",
    ),
]


class ToyQABenchmark:
    """Loader for the toy QA dataset."""

    name = "toy_qa"

    def load(self, limit: int | None = None) -> list[Example]:
        """Return the toy examples, optionally truncated to ``limit`` items."""
        if limit is None:
            return list(_EXAMPLES)
        if limit < 1:
            raise ValueError(f"limit must be >= 1, got {limit}")
        return list(_EXAMPLES[:limit])

    def __len__(self) -> int:
        return len(_EXAMPLES)
