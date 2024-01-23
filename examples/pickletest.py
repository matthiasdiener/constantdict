from pickle import dump, load

from constantdict import constantdict

i1 = constantdict({"a": "1", "b": "2", "c": "3"})
hash(i1)  # Force creating a cached hash value

try:
    # Second run: load pickle file
    with open("pickle_imm.pkl", "rb") as f:
        i2 = load(f)
except FileNotFoundError:
    # First run: create pickle file
    i2 = constantdict({"a": "1", "b": "2", "c": "3"})
    with open("pickle_imm.pkl", "wb") as f:
        dump(i1, f)

assert i1 == i2
print(hash(i1), hash(i2))
assert hash(i1) == hash(i2)

assert isinstance(i1, constantdict)
assert isinstance(i2, constantdict)
