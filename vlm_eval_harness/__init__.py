"""vlm-eval-harness: a CLI-first harness for evaluating VLMs / multimodal LLMs.

This package provides a small, honest vertical slice:

- a pluggable model-adapter interface (:mod:`vlm_eval_harness.models`),
- a tiny in-repo toy benchmark (:mod:`vlm_eval_harness.benchmarks`),
- exact-match metrics (:mod:`vlm_eval_harness.evaluation`),
- unified JSON / JSONL / CSV logging (:mod:`vlm_eval_harness.logging`),
- and a Typer-based CLI (:mod:`vlm_eval_harness.cli`).

Only the trivial ``echo`` model and ``toy_qa`` benchmark are implemented so far;
everything else is intentionally left as TODO rather than faked.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
