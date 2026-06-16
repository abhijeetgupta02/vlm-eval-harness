#!/usr/bin/env python3
"""Example: run the toy_qa benchmark with the echo model via the core API.

This mirrors what ``vlm-eval run --config configs/toy_qa_echo.yml`` does, but
calls into the Python API directly so you can see how to embed the harness.

Usage:
    python scripts/run_toy_qa.py [path/to/config.yml]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running directly from a checkout without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vlm_eval_harness.config import load_config  # noqa: E402
from vlm_eval_harness.core import run_evaluation  # noqa: E402

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "configs" / "toy_qa_echo.yml"


def main() -> None:
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONFIG
    config = load_config(config_path)
    summary = run_evaluation(config)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
