import pytest

from constantdict import constantdict


def test_basic() -> None:
    d = {"a": 1, "b": 2}
    cd = constantdict(d)
    assert cd == d

    assert isinstance(d, dict)
    assert isinstance(cd, dict)
    assert not isinstance(d, constantdict)
    assert isinstance(cd, constantdict)


def test_repr() -> None:
    cd = constantdict({"a": 1, "b": 2})
    assert repr(cd) == "constantdict({'a': 1, 'b': 2})"


def test_fromkeys() -> None:
    cd: constantdict[str, None] = constantdict.fromkeys(["a", "b", "c"])
    assert cd == {"a": None, "b": None, "c": None}
    assert cd == dict.fromkeys(["a", "b", "c"])


def test_set_delete_update() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    assert (cd.set("a", 10) == constantdict(a=10, b=2)
            == dict(a=10, b=2))  # noqa: C408
    assert cd.delete("a") == constantdict(b=2) == dict(b=2)  # noqa: C408

    assert isinstance(cd.set("a", 10), constantdict)
    assert isinstance(cd.delete("a"), constantdict)
    assert isinstance(cd.update({"a": 10}), constantdict)

    with pytest.raises(KeyError):
        cd.delete("c")

    assert cd.update({"a": 3}) == constantdict(a=3, b=2) == {"a": 3, "b": 2}

    assert (
        cd.update({"c": 17})
        == constantdict(a=1, b=2, c=17)
        == {"a": 1, "b": 2, "c": 17}
    )

    # Make sure 'd' has not changed
    assert cd == constantdict(a=1, b=2) == {"a": 1, "b": 2}
    assert isinstance(cd, constantdict)


def test_or() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    assert cd | {"a": 10} == constantdict(a=10, b=2) == {"a": 10, "b": 2}
    assert (cd | {"c": 17} == constantdict(a=1, b=2, c=17)
            == {"a": 1, "b": 2, "c": 17})

    assert isinstance(cd | {"a": 10}, constantdict)
    assert isinstance(cd | {"c": 17}, constantdict)
    assert not isinstance({"a": 10} | cd, constantdict)

    assert isinstance(cd | cd, constantdict)
    assert cd | cd == cd

    with pytest.raises(TypeError):
        cd | "a"

    with pytest.raises(TypeError):
        cd | 1

    with pytest.raises(TypeError):
        cd | None


def test_copy() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    assert cd.copy() == cd
    assert cd.copy() is not cd
    assert isinstance(cd.copy(), constantdict)


def test_hash() -> None:
    cd: constantdict[int, int] = constantdict({1: 2})

    assert hash(cd)


# {{{ test removed methods

def test_setitem() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd["a"] = 10


def test_delitem() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        del cd["a"]


def test_clear() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd.clear()


def test_ior() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd |= {"a": 10}  # type: ignore[has-type]


def test_popitem() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd.popitem()  # type: ignore[has-type]


def test_pop() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd.pop("a")  # type: ignore[has-type]

# }}}
