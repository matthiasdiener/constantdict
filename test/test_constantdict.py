from constantdict import constantdict


def test_basic() -> None:
    d = {"a": 1, "b": 2}
    cd = constantdict(d)
    assert cd == d


def test_fromkeys() -> None:
    cd = constantdict.fromkeys(["a", "b", "c"])
    assert cd == {"a": None, "b": None, "c": None}
    assert cd == dict.fromkeys(["a", "b", "c"])
