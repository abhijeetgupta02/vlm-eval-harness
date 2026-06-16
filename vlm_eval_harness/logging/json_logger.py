"""Unified JSON / JSONL / CSV logging.

A run produces three files in its output directory:

- ``records.jsonl`` -- one JSON object per evaluated example.
- ``records.csv``   -- the same per-example records as CSV.
- ``summary.json``  -- aggregated metrics plus run metadata.

Per-example records use the schema:
``{id, question, expected_answer, model_answer, correct}``.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExampleRecord:
    """One per-example log record."""

    id: str
    question: str
    expected_answer: str
    model_answer: str
    correct: bool


# Stable column / key order for both JSONL and CSV.
RECORD_FIELDS: tuple[str, ...] = (
    "id",
    "question",
    "expected_answer",
    "model_answer",
    "correct",
)


class JSONLogger:
    """Writes per-example records and an aggregate summary for one run."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def records_jsonl_path(self) -> Path:
        return self.output_dir / "records.jsonl"

    @property
    def records_csv_path(self) -> Path:
        return self.output_dir / "records.csv"

    @property
    def summary_path(self) -> Path:
        return self.output_dir / "summary.json"

    def write_records(self, records: list[ExampleRecord]) -> None:
        """Write all per-example records to JSONL and CSV."""
        with self.records_jsonl_path.open("w", encoding="utf-8") as fh:
            for record in records:
                fh.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")

        with self.records_csv_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(RECORD_FIELDS))
            writer.writeheader()
            for record in records:
                writer.writerow(asdict(record))

    def write_summary(self, summary: dict[str, Any]) -> None:
        """Write the aggregate summary JSON."""
        with self.summary_path.open("w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
