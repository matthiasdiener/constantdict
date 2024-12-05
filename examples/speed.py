# Simple speed test for various immutable dict implementations

from timeit import timeit
from typing import Mapping

from frozendict import frozendict
from immutabledict import immutabledict
from immutables import Map
from pyrsistent import pmap

from constantdict import constantdict

for N in (1, 1000):
    print(f"\n============= {N} items")
    for dict_impl in (dict, constantdict, immutabledict, Map, frozendict, pmap):

        # {{{ setup

        basedict = {str(i): i for i in range(N)}
        len_dict = len(basedict)

        # }}}

        name = dict_impl.__name__

        print(name)

        # {{{ Creation

        print("  init\t\t", timeit(f"{name}({basedict})",
                                    number=10000, globals=globals()))

        if name not in ("Map", "pmap"):
            print("  fromkeys\t", timeit(f"{name}.fromkeys(range(len_dict))",
                                        number=10000, globals=globals()))
        else:
            print("  fromkeys\t n/a")

        # }}}

        # {{{ Immutable operations

        if name != "dict":
            print("  hash\t\t", timeit(f"hash({name}({basedict}))",
                                    number=10000, globals=globals()))
        else:
            print("  hash\t\t n/a")

        if name != "dict":
            print("  hash2\t\t", timeit("for i in range(1000): hash(x)",
                                        setup=f"x={name}({basedict})",
                                        number=10000, globals=globals()))
        else:
            print("  hash2\t\t n/a")

        print("  elem_access\t", timeit(f"{name}({basedict})['0']",
                                        number=10000, globals=globals()))

        print("  list(keys)\t", timeit(f"list({name}({basedict}).keys())",
                                    number=10000, globals=globals()))

        # }}}

        # {{{ Mutation

        d: Mapping[str, int] = dict_impl(basedict)

        if name == "dict":
            mut_code = "d2 = d.copy(); d2[1] = 1"
        else:
            mut_code = "d2 = d.set(1, 1)"

        try:
            print("  copy+mutate\t", timeit(f"{mut_code}", number=10000,
                                            globals=globals()))
        except AttributeError:
            print("  copy+mutate\t n/a")

        # }}}
