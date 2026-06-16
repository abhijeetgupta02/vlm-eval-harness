# VLM Eval Harness

CLI-first Python harness for evaluating **vision-language models (VLMs)** and **multimodal LLMs** across multiple benchmarks with unified logging and reports.

> Status: ✨ Planning / scaffolding — API and benchmark list may evolve.

## Goals

- Provide a **single CLI** to run multiple VLM benchmarks.
- Support both **hosted APIs** (e.g., OpenAI, Anthropic) and **local models**.
- Log results in a **unified JSON / CSV schema** for leaderboard analysis.
- Make it easy to plug in **new tasks, prompts, and models**.

## Planned Features

- `vlm-eval run \` with:
  - `--benchmark` (or `--suite`) flag
  - `--model` / `--provider` (`openai`, `local`, etc.)
  - `--config` YAML for prompts, decoding, and logging
- Built-in adapters for common VLM / MLLM APIs
- Evaluation datasets wired through the [`awesome-vlm-evaluation`](https://github.com/abhijeetgupta02/awesome-vlm-evaluation) list
- Simple Python API on top of the CLI

## Repository Layout (planned)

```text
vlm-eval-harness/
  vlm_eval/
    cli.py           # Typer / Click CLI entrypoint
    config.py        # Pydantic / OmegaConf config definitions
    models/          # Model adapters (OpenAI, local, etc.)
    benchmarks/      # Benchmark runners and task definitions
    logging/         # JSON / CSV logging utilities
    evaluation/      # Metric computation, aggregation
  scripts/
    run_benchmark.py # Example invocations
  configs/
    openai-gpt4o.yml
    local-llava.yml
  tests/
  README.md
  pyproject.toml
```

## Getting Started

This repository is currently in the **design and scaffolding** phase.

Planned steps:

1. Finalize the minimal benchmark set and logging schema.
2. Implement a thin model adapter interface.
3. Add 1–2 reference configs and example runs.
4. Tag an `0.1.0` pre-release once something reproducible and useful exists.

If you are interested in collaborating, feel free to open an issue with suggestions on:

- Benchmarks you would like to see wired in first.
- Model providers you care about.
- Logging / schema constraints you need for your own analysis.
