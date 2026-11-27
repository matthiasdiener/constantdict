"""Benchmark read, construction, and hashing operations on several mappings."""

from __future__ import annotations

import builtins
import json
from collections.abc import Callable
from statistics import median
from timeit import Timer
from typing import Any

from frozendict import frozendict as pypi_frozendict
from immutabledict import immutabledict
from immutables import Map
from pyrsistent import pmap

from constantdict import constantdict


def implementations() -> dict[str, Callable[[dict[str, int]], Any]]:
    factories = {
        "dict": dict,
        "constantdict": constantdict,
        "Built-in frozendict": getattr(builtins, "frozendict", None),
        "immutabledict": immutabledict,
        "immutables.Map": Map,
        "PyPI frozendict": pypi_frozendict,
        "pyrsistent.PMap": pmap,
    }
    return {
        label: factory for label, factory in factories.items() if factory is not None
    }


def time_operation(statement: str, scope: dict[str, Any], executions: int) -> float:
    """Return the median time per execution in microseconds."""
    samples = Timer(statement, globals=scope).repeat(repeat=5, number=executions)
    return median(samples) * 1_000_000 / executions


def benchmark() -> dict[int, dict[str, dict[str, float | None]]]:
    results: dict[int, dict[str, dict[str, float | None]]] = {}
    for size in (1, 1_000):
        source = {str(i): i for i in range(size)}
        keys = range(size)
        results[size] = {}

        for label, factory in implementations().items():
            mapping = factory(source)
            operations = {
                "Build from dict": "factory(source)",
                "Look up a key": "mapping['0']",
                "List keys": "list(mapping.keys())",
                "fromkeys": (
                    "factory.fromkeys(keys)" if hasattr(factory, "fromkeys") else None
                ),
                "Build + first hash": (
                    "hash(factory(source))" if label != "dict" else None
                ),
                "Warm hash": "hash(mapping)" if label != "dict" else None,
            }
            if operations["Warm hash"] is not None:
                hash(mapping)

            scope = {
                "factory": factory, "source": source, "mapping": mapping, "keys": keys
            }
            results[size][label] = {
                name: time_operation(statement, scope, executions=10_000)
                    if statement is not None else None
                for name, statement in operations.items()
            }

    return results


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2))
