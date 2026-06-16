"""Typer-based CLI entrypoint: ``vlm-eval``.

Example
-------
    vlm-eval run --benchmark toy_qa --model echo --config configs/toy_qa_echo.yml
"""

from __future__ import annotations

from pathlib import Path

import typer

from . import __version__
from .benchmarks import available_benchmarks
from .config import RunConfig, load_config, merge_overrides
from .core import run_evaluation
from .models import available_models

app = typer.Typer(
    add_completion=False,
    help="CLI-first harness for evaluating VLMs / multimodal LLMs.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"vlm-eval-harness {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    _version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the harness version and exit.",
    ),
) -> None:
    """vlm-eval: run VLM benchmarks with unified logging."""


@app.command("list")
def list_components() -> None:
    """List registered benchmarks and model adapters."""
    typer.echo("Benchmarks: " + ", ".join(available_benchmarks()))
    typer.echo("Models:     " + ", ".join(available_models()))


@app.command()
def run(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        help="Path to a YAML run config.",
    ),
    benchmark: str | None = typer.Option(
        None,
        "--benchmark",
        "-b",
        help="Benchmark name; overrides the config file.",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="Model-adapter name; overrides the config file.",
    ),
    output_dir: str | None = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Output directory; overrides the config file.",
    ),
    limit: int | None = typer.Option(
        None,
        "--limit",
        "-n",
        min=1,
        help="Cap the number of examples; overrides the config file.",
    ),
) -> None:
    """Run an evaluation and write JSON / JSONL / CSV logs."""
    cfg: RunConfig = load_config(config)
    cfg = merge_overrides(
        cfg,
        benchmark=benchmark,
        model=model,
        output_dir=output_dir,
        limit=limit,
    )

    run_dir = Path(cfg.output_dir) / cfg.effective_run_name
    typer.echo(
        f"Running benchmark={cfg.benchmark!r} model={cfg.model!r} -> {run_dir}"
    )
    try:
        summary = run_evaluation(cfg)
    except (KeyError, RuntimeError, ValueError) as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    metrics = summary["metrics"]
    typer.echo(
        "Done: "
        f"{metrics['num_correct']}/{metrics['num_examples']} correct "
        f"(accuracy={metrics['accuracy']:.3f})"
    )
    typer.echo(f"Logs written to {summary['output_dir']}/")


if __name__ == "__main__":  # pragma: no cover
    app()
