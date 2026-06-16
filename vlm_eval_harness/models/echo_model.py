"""A trivial, deterministic ``echo`` model adapter.

This adapter does NOT pretend to be a real VLM. It echoes each question back
with a fixed prefix. Its only purpose is to exercise the full pipeline end to
end without network access, API keys, or fabricated accuracy. Because it never
actually answers the questions, its measured accuracy on a real benchmark will
typically be 0 -- which is the honest result for a model that only echoes.
"""

from __future__ import annotations

from typing import Any

from .base import BaseModelAdapter


class EchoModelAdapter(BaseModelAdapter):
    """Echoes the input question with a deterministic prefix."""

    name = "echo"

    def __init__(self, prefix: str = "ECHO: ") -> None:
        self.prefix = prefix

    def generate(self, inputs: list[dict[str, Any]]) -> list[str]:
        outputs: list[str] = []
        for item in inputs:
            question = str(item.get("question", ""))
            outputs.append(f"{self.prefix}{question}")
        return outputs
