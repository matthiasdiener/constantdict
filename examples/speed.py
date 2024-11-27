# Simple speed test for various immutable dict implementations

from timeit import timeit

from frozendict import frozendict
from immutabledict import immutabledict
from immutables import Map
from pyrsistent import pmap

from constantdict import constantdict

# Case 1: 1 item
basedict = {1: None}

# Case 2: 1000 items
# basedict = dict.fromkeys(range(1000))

len_dict = len(basedict)

for dict_impl in (dict, constantdict, immutabledict, Map, frozendict, pmap):

    name = dict_impl.__name__

    print(name)

    print("  creation\t", timeit(f"{name}({basedict})",
                                 number=10000, globals=globals()))

    try:
        print("  fromkeys\t", timeit(f"{name}.fromkeys(range(len_dict))",
                                     number=10000, globals=globals()))
    except AttributeError:
        print("  fromkeys MISSING")

    try:
        print("  hash\t\t", timeit(f"hash({name}({basedict}))",
                                   number=10000, globals=globals()))
    except (AttributeError, TypeError):
        print("  hash MISSING")

    try:
        print("  hash2\t\t", timeit("for i in range(1000): hash(x)",
                                    setup=f"x={name}({basedict})",
                                    number=10000, globals=globals()))
    except (AttributeError, TypeError):
        print("  hash2 MISSING")

    print("  elem_access\t", timeit(f"{name}({basedict})[1]",
                                    number=10000, globals=globals()))

    print("  list(keys)\t", timeit(f"list({name}({basedict}).keys())",
                                   number=10000, globals=globals()))
