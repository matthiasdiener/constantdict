from __future__ import annotations

import builtins
import pickle
import sys
from typing import Any

import pytest

from constantdict import constantdict, constantdictuncachedhash

pytestmark = [
    pytest.mark.skipif(sys.version_info < (3, 15), reason="requires Python 3.15"),
    pytest.mark.parametrize(
        "constantdict_type", [constantdict, constantdictuncachedhash]
    ),
]

frozendict: Any = getattr(builtins, "frozendict", None)


def test_equality_and_hash(constantdict_type: type[constantdict[str, Any]]) -> None:
    cd = constantdict_type(a=1, b=2)
    fd = frozendict(b=2, a=1)
    different = frozendict(b=3, a=1)

    assert cd == fd
    assert fd == cd
    assert cd != different
    assert different != cd
    assert hash(cd) == hash(fd)
    assert hash(constantdict_type()) == hash(frozendict())
    assert {cd: "cached"}[fd] == "cached"
    assert {fd: "cached"}[cd] == "cached"


def test_conversions_preserve_order(
        constantdict_type: type[constantdict[str, Any]]) -> None:
    items = [("b", 2), ("a", 1)]
    cd = constantdict_type(items)
    fd = frozendict(items)

    assert list(constantdict_type(fd).items()) == items
    assert list(frozendict(cd).items()) == items
    assert list(dict(cd).items()) == items
    assert list(dict(fd).items()) == items


def test_unhashable_values(constantdict_type: type[constantdict[str, Any]]) -> None:
    cd = constantdict_type(items=[1, 2])
    fd = frozendict(items=[1, 2])

    assert cd == fd
    with pytest.raises(TypeError, match="unhashable type"):
        hash(cd)
    with pytest.raises(TypeError, match="unhashable type"):
        hash(fd)


def test_nested_mappings(constantdict_type: type[constantdict[str, Any]]) -> None:
    cd = constantdict_type(inner=frozendict(b=2, a=1))
    fd = frozendict(inner=constantdict_type(a=1, b=2))

    assert cd == fd
    assert fd == cd
    assert hash(cd) == hash(fd)


def test_union_and_update(constantdict_type: type[constantdict[str, Any]]) -> None:
    cd = constantdict_type(a=1, b=2)
    fd = frozendict(b=3, c=4)

    merged = cd | fd
    assert type(merged) is constantdict_type
    assert list(merged.items()) == [("a", 1), ("b", 3), ("c", 4)]

    reverse = fd | cd
    assert type(reverse) is frozendict
    assert list(reverse.items()) == [("b", 2), ("c", 4), ("a", 1)]

    updated = cd.update(fd)
    assert type(updated) is constantdict_type
    assert list(updated.items()) == list(merged.items())

    augmented = cd
    augmented |= fd
    assert type(augmented) is constantdict_type
    assert list(augmented.items()) == list(merged.items())
    assert list(cd.items()) == [("a", 1), ("b", 2)]
    assert list(fd.items()) == [("b", 3), ("c", 4)]


def test_mutate_and_finish(constantdict_type: type[constantdict[str, Any]]) -> None:
    cd = constantdict_type(frozendict(a=1, b=2))
    mutation = cd.mutate()
    mutation.update(frozendict(b=3, c=4))
    result = mutation.finish()
    expected = frozendict(a=1, b=3, c=4)

    assert result is mutation
    assert type(result) is constantdict_type
    assert result == expected
    assert hash(result) == hash(expected)
    assert cd == frozendict(a=1, b=2)


def test_pickle_roundtrip(constantdict_type: type[constantdict[str, Any]]) -> None:
    cd = constantdict_type(inner=frozendict(b=2, a=1))
    restored = pickle.loads(pickle.dumps(cd))

    assert type(restored) is constantdict_type
    assert type(restored["inner"]) is frozendict
    assert list(restored["inner"].items()) == [("b", 2), ("a", 1)]
    assert restored == cd
    assert hash(restored) == hash(cd)
