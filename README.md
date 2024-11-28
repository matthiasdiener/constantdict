[![PyPI version](https://badge.fury.io/py/constantdict.svg)](https://badge.fury.io/py/constantdict)
[![Doc Status](https://img.shields.io/github/actions/workflow/status/matthiasdiener/constantdict/doc.yaml?label=docs)](https://matthiasdiener.github.io/constantdict)
[![License](https://img.shields.io/pypi/l/constantdict)](https://github.com/matthiasdiener/constantdict/blob/main/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/constantdict)](https://badge.fury.io/py/constantdict)

# constantdict

An immutable dictionary class for Python, implemented as a thin layer around Python's builtin `dict` class. It is often [faster than other immutable dictionary implementations](https://matthiasdiener.github.io/constantdict/speed.html).

## Usage

Install this package with:
```
$ pip install constantdict
```

Usage example:
```python
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
```

Please also see the [documentation](https://matthiasdiener.github.io/constantdict),
as well as the examples in the `examples/` directory.


## References

### Other packages

- [immutabledict](https://github.com/corenting/immutabledict)
- [immutables](https://github.com/MagicStack/immutables)
- [pyrsistent](https://github.com/tobgu/pyrsistent)
- [frozendict (old)](https://github.com/slezica/python-frozendict)
- [frozendict (new)](https://github.com/Marco-Sulla/python-frozendict)


### PEPs

- [PEP 416](https://www.python.org/dev/peps/pep-0416/)
- [PEP 603](https://www.python.org/dev/peps/pep-0603/)

## License

MIT License.
