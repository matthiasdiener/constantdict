"""Render PNG and PDF charts from the JSON produced by the benchmark examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Annotation
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

COLORS = {
    "dict": "#475569",
    "constantdict": "#c3422b",
    "Built-in frozendict": "#1261a0",
    "immutabledict": "#8d680b",
    "immutables.Map": "#2f7548",
    "PyPI frozendict": "#087b82",
    "pyrsistent.PMap": "#7854a1",
}


def chart(title: str, ylabel: str) -> tuple[Figure, Axes]:
    figure, axis = plt.subplots(figsize=(10, 5))
    figure.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.73)
    figure.suptitle(title, x=0.11, y=0.96, ha="left", fontsize=18, weight="bold")
    axis.set_ylabel(ylabel)
    axis.set_yscale("log")
    axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.set_axisbelow(True)
    axis.grid(axis="y", color="#dfe3e8")
    return figure, axis


def save(figure: Figure, output: Path) -> None:
    legend = figure.legend(
        loc="upper center", bbox_to_anchor=(0.5, 0.9), ncols=4, frameon=False
    )
    label = next(
        text for text in legend.get_texts() if text.get_text() == "constantdict"
    )
    label.set_fontweight("bold")
    # Anchor the underline to the label so it follows the PNG and PDF layouts.
    figure.add_artist(Annotation(
        "", xy=(0, 0), xycoords=label, xytext=(1, 0), textcoords=label,
        arrowprops={
            "arrowstyle": "-", "shrinkA": 0, "shrinkB": 0,
            "linewidth": 0.8, "color": label.get_color(),
        },
        annotation_clip=False, zorder=legend.get_zorder() + 1,
    ))

    for suffix in (".png", ".pdf"):
        figure.savefig(output.with_suffix(suffix), dpi=160)
    plt.close(figure)


def plot_bars(axis: Axes, results: dict[str, dict[str, float | None]]) -> None:
    categories = list(next(iter(results.values())))
    spacing = 0.8 / len(results)
    width = spacing * 0.9
    measured = [value for row in results.values() for value in row.values()
                if value is not None]
    baseline = min(measured) / 1.5
    axis.set_ylim(baseline, max(measured) * 1.6)

    for index, (label, row) in enumerate(results.items()):
        offset = (index - (len(results) - 1) / 2) * spacing
        positions = []
        heights = []
        for index_in_group, category in enumerate(categories):
            position = index_in_group + offset
            value = row[category]
            if value is None:
                axis.text(position, baseline * 1.06, "n/a", ha="center", va="bottom",
                          fontsize=7, color="#475569")
            else:
                positions.append(position)
                heights.append(value - baseline)
        axis.bar(positions, heights, width, bottom=baseline,
                 color=COLORS[label], label=label)

    axis.set_xticks(range(len(categories)), categories)


def plot_operations(
        results: dict[str, dict[str, float | None]], size: int, output: Path,
) -> None:
    figure, axis = chart(
        f"Non-mutating operations on {size:,} {'item' if size == 1 else 'items'}",
        "Time per operation (μs, log scale)",
    )
    plot_bars(axis, results)
    save(figure, output)


def plot_mutation(results: dict[str, dict[str, float | None]], output: Path) -> None:
    figure, axis = chart(
        "Ten lookups followed by one functional update",
        "Time per iteration (μs, log scale)",
    )
    sizes = sorted(int(size) for size in results)
    plot_bars(axis, {
        label: {f"{size:,}": results[str(size)].get(label) for size in sizes}
        for label in COLORS if any(label in row for row in results.values())
    })
    axis.set_xlabel("Number of items before the update")
    axis.yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    axis.yaxis.set_minor_formatter(NullFormatter())
    save(figure, output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operations", type=Path, help="JSON from examples/speed.py")
    parser.add_argument(
        "mutation", type=Path, help="JSON from examples/speed_mutation.py"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plt.switch_backend("Agg")

    operations = json.loads(args.operations.read_text())
    plot_operations(operations["1"], 1, args.output_dir / "dict_performance_small")
    plot_operations(
        operations["1000"], 1_000, args.output_dir / "dict_performance_large"
    )
    plot_mutation(
        json.loads(args.mutation.read_text()),
        args.output_dir / "dict_performance_mutation",
    )


if __name__ == "__main__":
    main()
