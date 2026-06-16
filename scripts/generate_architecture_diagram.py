#!/usr/bin/env python3
"""Generate the architecture diagram for the VLM Eval Harness.

Renders the component flow to ``docs/architecture.png`` using matplotlib (no
system Graphviz needed). The diagram is purely structural -- it shows how the
pieces connect and contains no metrics or results.

Flow (matches ``vlm_eval_harness/core.run_evaluation``):

    CLI (vlm-eval) -> Config -> Benchmark -> Model Adapter -> Evaluation
    -> Logging (JSON/JSONL/CSV)

Usage:
    python scripts/generate_architecture_diagram.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: write a file, never open a window
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "docs" / "architecture.png"

# (title, subtitle) for each stage, in execution order.
STAGES = [
    ("CLI", "vlm-eval run"),
    ("Config", "RunConfig + YAML"),
    ("Benchmark", "toy_qa.load()"),
    ("Model Adapter", "echo.generate()"),
    ("Evaluation", "exact_match"),
    ("Logging", "JSON / JSONL / CSV"),
]

BOX_W, BOX_H, GAP = 2.4, 1.3, 0.9
FILL, EDGE = "#e8f0fe", "#1a73e8"


def main() -> None:
    n = len(STAGES)
    fig_w = n * BOX_W + (n - 1) * GAP + 1.0
    fig, ax = plt.subplots(figsize=(fig_w, 2.6))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, 2.6)
    ax.axis("off")

    y = 1.3
    centers = []
    for i, (title, subtitle) in enumerate(STAGES):
        x = 0.5 + i * (BOX_W + GAP)
        ax.add_patch(
            FancyBboxPatch(
                (x, y - BOX_H / 2),
                BOX_W,
                BOX_H,
                boxstyle="round,pad=0.02,rounding_size=0.12",
                linewidth=1.6,
                edgecolor=EDGE,
                facecolor=FILL,
            )
        )
        cx = x + BOX_W / 2
        ax.text(cx, y + 0.18, title, ha="center", va="center",
                fontsize=12, fontweight="bold", color="#202124")
        ax.text(cx, y - 0.28, subtitle, ha="center", va="center",
                fontsize=9, color="#5f6368", family="monospace")
        centers.append((x, cx))

    for i in range(n - 1):
        x_start = centers[i][0] + BOX_W
        x_end = centers[i + 1][0]
        ax.add_patch(
            FancyArrowPatch(
                (x_start, y),
                (x_end, y),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=1.6,
                color="#5f6368",
            )
        )

    ax.set_title("VLM Eval Harness — component flow", fontsize=13, pad=12)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=150, bbox_inches="tight")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
