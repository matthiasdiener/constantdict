"""Benchmark a workload of ten reads followed by one functional update."""

from __future__ import annotations

import json

from speed import implementations, time_operation


def benchmark() -> dict[int, dict[str, float | None]]:
    results: dict[int, dict[str, float | None]] = {}
    lookups = "mapping.get('0')\n" * 10
    change = {"new": -1}

    for size in (10, 100, 1_000):
        source = {str(i): i for i in range(size)}
        results[size] = {}

        for label, factory in implementations().items():
            mapping = factory(source)
            if label == "dict":
                update = "result = mapping.copy(); result.update(change)"
            elif label == "Built-in frozendict":
                update = "result = mapping | change"
            elif label == "PyPI frozendict":
                update = "result = mapping.set('new', -1)"
            elif hasattr(mapping, "update"):
                update = "result = mapping.update(change)"
            else:
                results[size][label] = None
                continue

            results[size][label] = time_operation(
                lookups + update, {"mapping": mapping, "change": change},
                executions=100_000,
            )

    return results


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2))
