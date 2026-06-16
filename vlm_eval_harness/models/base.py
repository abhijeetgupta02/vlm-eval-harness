"""Abstract model-adapter interface.

A model adapter turns a list of benchmark inputs into a list of text answers.
Inputs are plain dicts so adapters can evolve (adding image paths, options,
etc.) without breaking the interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseModelAdapter(ABC):
    """Minimal interface every model adapter must implement.

    An input item is a dict with at least a ``"question"`` key. Adapters may
    also read ``"image"`` (a path or placeholder id) and any other fields a
    benchmark chooses to provide.
    """

    #: Short, registry-friendly identifier for the adapter.
    name: str = "base"

    @abstractmethod
    def generate(self, inputs: list[dict[str, Any]]) -> list[str]:
        """Return one text answer per input item, in the same order.

        Implementations MUST return exactly ``len(inputs)`` strings so that
        downstream scoring can align answers with expected values.
        """
        raise NotImplementedError

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{type(self).__name__}(name={self.name!r})"
