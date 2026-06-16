"""Benchmarks and a tiny name-based registry."""

from __future__ import annotations

from typing import Callable, Protocol, runtime_checkable

from .toy_qa import Example, ToyQABenchmark


@runtime_checkable
class Benchmark(Protocol):
    """Structural type every benchmark loader must satisfy."""

    name: str

    def load(self, limit: int | None = ...) -> list[Example]:
        ...


# Map of registry name -> zero-arg factory returning a fresh benchmark instance.
_REGISTRY: dict[str, Callable[[], Benchmark]] = {
    "toy_qa": ToyQABenchmark,
}


def available_benchmarks() -> list[str]:
    """Return the sorted list of registered benchmark names."""
    return sorted(_REGISTRY)


def get_benchmark(name: str) -> Benchmark:
    """Instantiate a registered benchmark by name."""
    try:
        factory = _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"Unknown benchmark {name!r}. "
            f"Available benchmarks: {available_benchmarks()}"
        ) from None
    return factory()


__all__ = [
    "Benchmark",
    "Example",
    "ToyQABenchmark",
    "available_benchmarks",
    "get_benchmark",
]
