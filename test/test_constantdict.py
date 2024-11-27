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


def test_set_delete_remove_update() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    assert (cd.set("a", 10) == constantdict(a=10, b=2)
            == dict(a=10, b=2))  # noqa: C408
    assert (cd.remove("a") == cd.delete("a")
            == constantdict(b=2) == dict(b=2))  # noqa: C408

    assert isinstance(cd.set("a", 10), constantdict)
    assert isinstance(cd.delete("a"), constantdict)
    assert isinstance(cd.remove("a"), constantdict)
    assert isinstance(cd.update({"a": 10}), constantdict)

    with pytest.raises(KeyError):
        cd.delete("c")

    with pytest.raises(KeyError):
        cd.remove("c")

    assert cd.update({"a": 3}) == constantdict(a=3, b=2) == {"a": 3, "b": 2}

    assert (
        cd.update({"c": 17})
        == constantdict(a=1, b=2, c=17)
        == {"a": 1, "b": 2, "c": 17}
    )

    # Make sure 'cd' has not changed
    assert cd == constantdict(a=1, b=2) == {"a": 1, "b": 2}
    assert isinstance(cd, constantdict)


def test_or() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    assert cd | {"a": 10} == constantdict(a=10, b=2) == {"a": 10, "b": 2}
    assert (cd | {"c": 17} == constantdict(a=1, b=2, c=17)
            == {"a": 1, "b": 2, "c": 17})

    assert isinstance(cd | {"a": 10}, constantdict)
    assert isinstance(cd | {"c": 17}, constantdict)

    import sys
    if sys.version_info >= (3, 9):
        # | operator for dict was introduced in Python 3.9
        assert not isinstance({"a": 10} | cd, constantdict)
        assert isinstance({"a": 10} | cd, dict)

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

    # Hash must be independent of insertion order
    cd1 = constantdict({1: 2, 3: 4})
    cd2 = constantdict({3: 4, 1: 2})

    assert cd1 == cd2
    assert hash(cd1) == hash(cd2)

    # Keys and values should contribute to hash
    cd1 = constantdict({1: 2, 3: 4})
    cd2 = constantdict({1: 2, 3: 3})
    cd3 = constantdict({2: 2, 3: 4})

    assert cd1 != cd2 and cd1 != cd3 and cd2 != cd3
    assert (hash(cd1) != hash(cd2)
            and hash(cd1) != hash(cd3)
            and hash(cd2) != hash(cd3))


def test_discard() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    # Key present
    assert cd.discard("a") == constantdict(b=2) == {"b": 2}
    assert hash(cd.discard("a")) != hash(cd)

    # Key not present
    assert cd.discard("c") == cd == {"a": 1, "b": 2}
    assert hash(cd.discard("c")) == hash(cd)
    assert cd.discard("c") is cd


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
    if not hasattr(dict, "__ior__"):
        assert not hasattr(constantdict, "__ior__")
        pytest.skip("dict.__ior__ not available before Python 3.9")

    cd: constantdict[str, int] = constantdict(a=1, b=2)

    cdd = cd

    cd |= {"a": 10}

    assert cd == {"a": 10, "b": 2}
    assert cdd == {"a": 1, "b": 2}
    assert isinstance(cd, constantdict)
    assert cd is not cdd

    # dict behaves differently
    d: dict[str, int] = dict(a=1, b=2)

    dd = d

    d |= {"a": 10}

    assert d == {"a": 10, "b": 2}
    assert dd == {"a": 10, "b": 2}
    assert isinstance(d, dict)
    assert d is dd

    # frozenset behaves like constantdict:
    fs = frozenset([1, 2])
    fsd = fs
    fs |= {3}

    assert fs == frozenset([1, 2, 3])
    assert fsd == frozenset([1, 2])
    assert fs is not fsd


def test_popitem() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd.popitem()  # type: ignore[has-type]


def test_pop() -> None:
    cd: constantdict[str, int] = constantdict(a=1, b=2)

    with pytest.raises(AttributeError):
        cd.pop("a")  # type: ignore[has-type]

# }}}
