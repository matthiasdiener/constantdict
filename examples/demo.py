from constantdict import constantdict

cd = constantdict({1: 2})

# constantdicts compare equal to dicts with the same items
assert cd == {1: 2}

# constantdicts are hashable, and their hashes are cached
print(hash(cd), cd)

# Attempting to modify a constantdict in-place raises an AttributeError
try:
    # Similar for pop(), popitem(), clear(), and del
    cd[4] = 12
except AttributeError:
    pass

# Some methods return a mutated copy of a constantdict
cd_new = cd.setdefault(10, 5)
assert cd_new == {1: 2, 10: 5}
# Similar for set(), update(), delete(), discard()

# Performing multiple mutations can be faster via mutate()/finish()
cd_mut = cd.mutate()  # cd_mut is a mutable copy of cd
cd_mut[42] = 0
del cd_mut[1]
cd_new2 = cd_mut.finish()  # cd_new2 is an immutable version of cd_mut
assert cd_new2 == {42: 0}
