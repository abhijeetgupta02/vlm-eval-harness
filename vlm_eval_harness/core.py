"""Core evaluation runner shared by the CLI and the Python API.

This is the single place that wires a benchmark, a model adapter, the metric,
and the logger together. Keeping it free of CLI concerns lets scripts and tests
call :func:`run_evaluation` directly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import __version__
from .benchmarks import get_benchmark
from .config import RunConfig
from .evaluation import aggregate, exact_match
from .logging import ExampleRecord, JSONLogger
from .models import get_model


def run_evaluation(config: RunConfig) -> dict[str, Any]:
    """Run one evaluation described by ``config`` and write log files.

    Returns the summary dict that is also written to ``summary.json``. Every
    metric in the summary is computed from real model outputs.
    """
    benchmark = get_benchmark(config.benchmark)
    model = get_model(config.model)

    examples = benchmark.load(limit=config.limit)
    model_inputs = [example.to_model_input() for example in examples]
    answers = model.generate(model_inputs)

    if len(answers) != len(examples):
        raise RuntimeError(
            f"Model {config.model!r} returned {len(answers)} answers for "
            f"{len(examples)} examples; counts must match."
        )

    records: list[ExampleRecord] = []
    correct_flags: list[bool] = []
    for example, answer in zip(examples, answers):
        is_correct = exact_match(answer, example.expected_answer)
        correct_flags.append(is_correct)
        records.append(
            ExampleRecord(
                id=example.id,
                question=example.question,
                expected_answer=example.expected_answer,
                model_answer=answer,
                correct=is_correct,
            )
        )

    metrics = aggregate(correct_flags)

    run_dir = Path(config.output_dir) / config.effective_run_name
    logger = JSONLogger(run_dir)
    logger.write_records(records)

    summary: dict[str, Any] = {
        "harness_version": __version__,
        "benchmark": config.benchmark,
        "model": config.model,
        "run_name": config.effective_run_name,
        "metrics": metrics.as_dict(),
        "output_dir": str(run_dir),
    }
    logger.write_summary(summary)
    return summary
