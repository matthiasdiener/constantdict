from constantdict import constantdict

def test_from_keys() -> None:
    keys = ["a", "b", "c"]
    immutable_dict: constantdict[str, Any] = constantdict.fromkeys(keys)
    assert "a" in immutable_dict
    assert "b" in immutable_dict
    assert "c" in immutable_dict

def test_init_and_compare() -> None:
    normal_dict = {"a": "value", "b": "other_value"}
    immutable_dict: constantdict[str, str] = constantdict(normal_dict)
    assert immutable_dict == normal_dict
