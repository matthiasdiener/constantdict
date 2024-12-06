# Based on https://gist.github.com/1st1/292e3f0bbe43bd65ff3256f80aa2637d

import time
from typing import Any, Dict

import frozendict
import immutabledict
import immutables
import pyrsistent

import constantdict

ITER = 1_000_000
KEY = "5"


for N in (5, 10, 20, 30, 100, 200, 300, 400, 500, 1000):
    print("=============")
    print(f"  # of items: {N}; iterations: {ITER}")
    print()

    cd: constantdict.constantdict[str, Any] = constantdict.constantdict()
    h: immutables.Map[str, Any] = immutables.Map()
    d: Dict[str, Any] = {}
    pm: Any = pyrsistent.pmap()
    idd: immutabledict.immutabledict[str, Any] = immutabledict.immutabledict()
    fd: Any = frozendict.frozendict()

    for i in range(N):
        cd = cd.set(str(i), i)
        h = h.set(str(i), i)
        pm = pm.set(str(i), i)
        d[str(i)] = i
        if hasattr(idd, "set"):
            idd = idd.set(str(i), i)
        fd = fd.set(str(i), i)

    assert len(h) == N
    assert len(d) == N
    assert len(pm) == N
    assert len(cd) == N
    if hasattr(idd, "set"):
        assert len(idd) == N
    assert len(fd) == N

    for i in range(N):
        assert h.get(str(i), "not found") == i

    st = time.monotonic()
    for _ in range(ITER):
        d.get(KEY)
        d.get(KEY)
        d.get(KEY)
        d.get(KEY)
        d.get(KEY)

        d.get(KEY)
        d.get(KEY)
        d.get(KEY)
        d.get(KEY)
        d.get(KEY)

        d2 = d.copy()
        d2.update({"aaa": "aaa"})
        # d2['aaa'] = 'aaa'
        # del d2['1']

    end = time.monotonic() - st
    print(f"  dict copy:\t\t\t{end:.4f}s")

    st = time.monotonic()
    for _ in range(ITER):
        h.get(KEY)
        h.get(KEY)
        h.get(KEY)
        h.get(KEY)
        h.get(KEY)

        h.get(KEY)
        h.get(KEY)
        h.get(KEY)
        h.get(KEY)
        h.get(KEY)

        # h2 = h.delete('aaa', 'aaa')
        # h2 = h.delete('1')
        h2 = h.update({"aaa": "aaa"})

    end = time.monotonic() - st
    print(f"  immutables.Map:\t\t{end:.4f}s")

    st = time.monotonic()
    for _ in range(ITER):
        pm.get(KEY)
        pm.get(KEY)
        pm.get(KEY)
        pm.get(KEY)
        pm.get(KEY)

        pm.get(KEY)
        pm.get(KEY)
        pm.get(KEY)
        pm.get(KEY)
        pm.get(KEY)

        # pm2 = pm.set('aaa', 'aaa')
        # pm2 = pm.delete('1')
        pm2 = pm.update({"aaa": "aaa"})

    end = time.monotonic() - st
    print(f"  pyrsistent.PMap:\t\t{end:.4f}s")

    if hasattr(idd, "set"):
        st = time.monotonic()
        for _ in range(ITER):
            idd.get(KEY)
            idd.get(KEY)
            idd.get(KEY)
            idd.get(KEY)
            idd.get(KEY)

            idd.get(KEY)
            idd.get(KEY)
            idd.get(KEY)
            idd.get(KEY)
            idd.get(KEY)

            # idd2 = idd.set('aaa', 'aaa')
            # idd2 = idd.delete('1')
            idd2 = idd.update({"aaa": "aaa"})

        end = time.monotonic() - st
        print(f"  immutabledict copy:\t\t{end:.4f}s")
    else:
        print("  immutabledict does not have a 'set' method, Skipping...")

    st = time.monotonic()
    for _ in range(ITER):
        cd.get(KEY)
        cd.get(KEY)
        cd.get(KEY)
        cd.get(KEY)
        cd.get(KEY)

        cd.get(KEY)
        cd.get(KEY)
        cd.get(KEY)
        cd.get(KEY)
        cd.get(KEY)

        # cd2 = cd.set('aaa', 'aaa')
        # cd2 = cd.delete('1')
        cd2 = cd.update({"aaa": "aaa"})

    end = time.monotonic() - st
    print(f"  constantdict copy:\t\t{end:.4f}s")

    st = time.monotonic()
    for _ in range(ITER):
        fd.get(KEY)
        fd.get(KEY)
        fd.get(KEY)
        fd.get(KEY)
        fd.get(KEY)

        fd.get(KEY)
        fd.get(KEY)
        fd.get(KEY)
        fd.get(KEY)
        fd.get(KEY)

        fd2 = fd.set("aaa", "aaa")
        # fd2 = fd.delete('1')
        # fd2 = fd.update({"aaa": "aaa"}) # n/a in frozendict

    end = time.monotonic() - st
    print(f"  frozendict copy:\t\t{end:.4f}s")
