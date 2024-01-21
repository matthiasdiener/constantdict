from constantdict import constantdict


cd = constantdict({1:2})

assert cd == {1:2}

print(hash(cd), cd)


assert constantdict.fromkeys([1,2,3]) == {1:None, 2:None, 3:None}


try:
    cd[4] = 12
except AttributeError:
    pass
else:
    raise AssertionError("Should have raised an AttributeError")
