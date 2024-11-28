from constantdict import constantdict

cd = constantdict({1: 2})

# constantdicts compare equal to dicts with the same items
assert cd == {1: 2}

# constantdicts are hashable, and their hashes are cached
print(hash(cd), cd)

# Attempting to modify the constantdict raises an AttributeError
try:
    # Similar for pop(), popitem(), clear(), del, and setdefault()
    cd[4] = 12
except AttributeError:
    pass
