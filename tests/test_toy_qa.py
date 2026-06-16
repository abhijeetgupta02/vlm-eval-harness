"""End-to-end tests for the toy_qa + echo pipeline via the core API."""

from __future__ import annotations

import json

from vlm_eval_harness.benchmarks import get_benchmark
from vlm_eval_harness.config import RunConfig
from vlm_eval_harness.core import run_evaluation
from vlm_eval_harness.evaluation import exact_match
from vlm_eval_harness.logging import RECORD_FIELDS
from vlm_eval_harness.models import get_model


def test_pipeline_runs_end_to_end(tmp_path):
    config = RunConfig(
        benchmark="toy_qa",
        model="echo",
        output_dir=str(tmp_path),
        run_name="t",
    )
    summary = run_evaluation(config)

    benchmark = get_benchmark("toy_qa")
    n = len(benchmark.load())

    assert summary["benchmark"] == "toy_qa"
    assert summary["model"] == "echo"
    assert summary["metrics"]["num_examples"] == n
    # Echo never answers correctly on toy_qa: honest accuracy is 0.0.
    assert summary["metrics"]["num_correct"] == 0
    assert summary["metrics"]["accuracy"] == 0.0


def test_log_files_created_with_expected_keys(tmp_path):
    config = RunConfig(
        benchmark="toy_qa", model="echo", output_dir=str(tmp_path), run_name="t"
    )
    run_evaluation(config)
    run_dir = tmp_path / "t"

    jsonl_path = run_dir / "records.jsonl"
    csv_path = run_dir / "records.csv"
    summary_path = run_dir / "summary.json"
    assert jsonl_path.is_file()
    assert csv_path.is_file()
    assert summary_path.is_file()

    lines = jsonl_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 5
    first = json.loads(lines[0])
    assert set(first.keys()) == set(RECORD_FIELDS)
    assert isinstance(first["correct"], bool)

    header = csv_path.read_text(encoding="utf-8").splitlines()[0]
    assert header.split(",") == list(RECORD_FIELDS)

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert set(summary["metrics"].keys()) == {
        "num_examples",
        "num_correct",
        "accuracy",
    }


def test_limit_truncates_examples(tmp_path):
    config = RunConfig(
        benchmark="toy_qa",
        model="echo",
        output_dir=str(tmp_path),
        run_name="t",
        limit=2,
    )
    summary = run_evaluation(config)
    assert summary["metrics"]["num_examples"] == 2


def test_echo_model_is_deterministic_echo():
    model = get_model("echo")
    out = model.generate([{"question": "hello"}, {"question": "world"}])
    assert out == ["ECHO: hello", "ECHO: world"]


def test_exact_match_normalizes():
    assert exact_match(" Blue. ", "blue")
    assert not exact_match("red", "blue")
