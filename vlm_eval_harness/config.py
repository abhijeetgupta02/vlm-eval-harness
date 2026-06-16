"""Configuration schema and YAML loader.

The config is intentionally tiny. It captures only what the first vertical
slice needs: which benchmark to run, which model adapter to use, and where to
write logs. No API keys or provider secrets live here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    """Validated configuration for a single evaluation run."""

    benchmark: str = Field(
        ...,
        description="Registered benchmark name, e.g. 'toy_qa'.",
    )
    model: str = Field(
        ...,
        description="Registered model-adapter name, e.g. 'echo'.",
    )
    output_dir: str = Field(
        "runs",
        description="Directory where per-run log files are written.",
    )
    run_name: str | None = Field(
        None,
        description="Optional human-readable name for this run; used in the "
        "output subdirectory. Defaults to '<benchmark>_<model>'.",
    )
    limit: int | None = Field(
        None,
        ge=1,
        description="Optional cap on the number of examples to evaluate. "
        "Useful for smoke tests. None means 'all examples'.",
    )

    # Forbid unknown keys so typos in YAML are caught early rather than ignored.
    model_config = {"extra": "forbid"}

    @property
    def effective_run_name(self) -> str:
        """Run name to use, falling back to '<benchmark>_<model>'."""
        return self.run_name or f"{self.benchmark}_{self.model}"


def load_config(path: str | Path) -> RunConfig:
    """Load and validate a :class:`RunConfig` from a YAML file."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        raw: Any = yaml.safe_load(fh) or {}
    if not isinstance(raw, dict):
        raise ValueError(
            f"Config root must be a mapping/object, got {type(raw).__name__}."
        )
    return RunConfig(**raw)


def merge_overrides(config: RunConfig, **overrides: Any) -> RunConfig:
    """Return a copy of ``config`` with any non-None ``overrides`` applied.

    This lets CLI flags (e.g. ``--benchmark``) take precedence over the YAML
    file without mutating the original config.
    """
    updates = {key: value for key, value in overrides.items() if value is not None}
    if not updates:
        return config
    return config.model_copy(update=updates)
