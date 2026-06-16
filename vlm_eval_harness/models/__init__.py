"""Model adapters and a tiny name-based registry.

New adapters register themselves here so the CLI / core runner can instantiate
them by name (e.g. ``--model echo``).
"""

from __future__ import annotations

from typing import Callable

from .base import BaseModelAdapter
from .echo_model import EchoModelAdapter

# Map of registry name -> zero-arg factory returning a fresh adapter instance.
_REGISTRY: dict[str, Callable[[], BaseModelAdapter]] = {
    "echo": EchoModelAdapter,
}


def available_models() -> list[str]:
    """Return the sorted list of registered model-adapter names."""
    return sorted(_REGISTRY)


def get_model(name: str) -> BaseModelAdapter:
    """Instantiate a registered model adapter by name."""
    try:
        factory = _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"Unknown model {name!r}. Available models: {available_models()}"
        ) from None
    return factory()


__all__ = [
    "BaseModelAdapter",
    "EchoModelAdapter",
    "available_models",
    "get_model",
]
