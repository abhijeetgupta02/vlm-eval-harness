"""CLI smoke tests using Typer's CliRunner."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from vlm_eval_harness.cli import app

runner = CliRunner()

CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "toy_qa_echo.yml"


def test_cli_rejects_unknown_flag(tmp_path):
    result = runner.invoke(
        app,
        [
            "run",
            "--config",
            str(CONFIG_PATH),
            "--output-dir",
            str(tmp_path),
            "--not-a-real-flag",
        ],
    )
    # Unknown flag should be rejected by Typer (non-zero exit).
    assert result.exit_code != 0


def test_cli_run_happy_path(tmp_path):
    result = runner.invoke(
        app,
        [
            "run",
            "--config",
            str(CONFIG_PATH),
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Done:" in result.output

    summary_path = tmp_path / "toy_qa_echo" / "summary.json"
    assert summary_path.is_file()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["benchmark"] == "toy_qa"
    assert summary["model"] == "echo"


def test_cli_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "toy_qa" in result.output
    assert "echo" in result.output


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "vlm-eval-harness" in result.output


def test_cli_unknown_model_errors(tmp_path):
    result = runner.invoke(
        app,
        [
            "run",
            "--config",
            str(CONFIG_PATH),
            "--model",
            "does_not_exist",
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 1
    assert "Error:" in result.output
