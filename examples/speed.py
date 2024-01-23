from timeit import timeit

from frozendict import frozendict
from immutabledict import immutabledict
from immutables import Map
from pyrsistent import pmap

from constantdict import constantdict

basedict = {1: None}
basedict = dict.fromkeys(range(1000))

for dict_impl in (dict, constantdict, immutabledict, Map, frozendict, pmap):
    print(dict_impl.__name__)

    print("  creation", timeit(f"{dict_impl.__name__}({basedict})",
                               number=10000, globals=globals()))

    try:
        print("  fromkeys", timeit(f"{dict_impl.__name__}.fromkeys(range(1000))",
                                   number=10000, globals=globals()))
    except AttributeError:
        print("  fromkeys MISSING")

    try:
        print("  hash", timeit(f"hash({dict_impl.__name__}({basedict}))",
                               number=10000, globals=globals()))
    except (AttributeError, TypeError):
        print("  hash MISSING")

    print("  elem_access", timeit(f"{dict_impl.__name__}({basedict})[1]",
                                  number=10000, globals=globals()))

    print("  list(keys)", timeit(f"list({dict_impl.__name__}({basedict}).keys())",
                                 number=10000, globals=globals()))
