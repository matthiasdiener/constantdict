from typing import Any

import pytest

from constantdict import constantdict


def test_basic() -> None:
    d = {"a": 1, "b": 2}
    cd = constantdict(d)
    assert cd == d


def test_repr() -> None:
    cd = constantdict({"a": 1, "b": 2})
    assert repr(cd) == "constantdict({'a': 1, 'b': 2})"


def test_fromkeys() -> None:
    cd: constantdict[Any, Any] = constantdict.fromkeys(["a", "b", "c"])
    assert cd == {"a": None, "b": None, "c": None}
    assert cd == dict.fromkeys(["a", "b", "c"])


def test_set_delete_update() -> None:
    d: constantdict[str, int] = constantdict(a=1, b=2)

    assert d.set("a", 10) == constantdict(a=10, b=2) == dict(a=10, b=2)  # noqa: C408
    assert d.delete("a") == constantdict(b=2) == dict(b=2)  # noqa: C408

    with pytest.raises(KeyError):
        d.delete("c")

    assert d.update({"a": 3}) == constantdict(a=3, b=2) == {"a": 3, "b": 2}

    assert (
        d.update({"c": 17})
        == constantdict(a=1, b=2, c=17)
        == {"a": 1, "b": 2, "c": 17}
    )

    # Make sure 'd' has not changed
    assert d == constantdict(a=1, b=2) == {"a": 1, "b": 2}
