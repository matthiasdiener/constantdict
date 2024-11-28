"""Immutable dictionary implementation."""

from __future__ import annotations

__copyright__ = """
Copyright (C) 2024 University of Illinois Board of Trustees
"""


__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    # Python 3.7
    import importlib_metadata  # type: ignore[no-redef]

__version__ = importlib_metadata.version(__package__ or __name__)


import sys
from typing import Any, Dict, TypeVar  # <3.9 needs Dict, not dict

K = TypeVar("K")
V = TypeVar("V")


def _del_attr(self: Any, *args: Any, **kwargs: Any) -> None:
    """Raise an AttributeError when trying to modify the object."""
    raise AttributeError("object is immutable")


class constantdict(Dict[K, V]):  # noqa: N801
    """An immutable dictionary that does not allow modifications after
    creation. This class behaves mostly like a :class:`dict`,
    but with the following differences.

    Additional methods compared to :class:`dict`:

    .. automethod:: __hash__

    Methods that return a modified copy of the :class:`constantdict`:

    .. automethod:: set
    .. automethod:: delete
    .. automethod:: update
    .. automethod:: discard

    Deleted methods compared to :class:`dict`
    (these raise an :exc:`AttributeError` when called):

    .. method:: __delitem__
    .. method:: __setitem__
    .. method:: clear
    .. method:: popitem
    .. method:: pop
    .. method:: setdefault
    """

    @classmethod
    def fromkeys(cls: type[dict[K, V]], *args: Any,
                 **kwargs: Any) -> Any:
        """Create a new :class:`constantdict` from supplied keys and values."""
        # dict.fromkeys calls __setitem__, hence need to convert from a 'dict'
        return cls(dict.fromkeys(*args, **kwargs))

    def __hash__(self) -> int:  # type: ignore[override]
        """Return a hash of this :class:`constantdict`. This
        :class:`constantdict` is hashable if all of its keys and values are
        hashable. Once computed, the hash is cached."""
        try:
            return self._hash
        except AttributeError:
            self._hash: int = hash(frozenset(self.items()))
            return self._hash

    def __repr__(self) -> str:
        """Return a string representation of this :class:`constantdict`."""
        return f"{self.__class__.__name__}({dict(self)!r})"

    def __reduce__(self) -> str | tuple[type, tuple[dict[K, V]]]:
        """Return pickling information for this :class:`constantdict`."""
        # Do not store the cached hash value when pickling
        # as the value might change across Python invocations.

        # Also, this circumvents pickle's internal calls to __setitem__,
        # which would raise an exception in constantdict.
        return (self.__class__, (dict(self),))

    if sys.version_info >= (3, 9):
        # Python 3.9 introduced __or__ and __ior__ for dict
        def __or__(self, other: object) -> constantdict[K, V]:  # type: ignore[override]
            """Return the union of this :class:`constantdict` and *other*."""
            if not isinstance(other, (dict, self.__class__)):
                return NotImplemented
            return self.update(other)

        # Like frozenset.__ior__, constantdict.__ior__ must return a new instance
        __ior__ = __or__  # type: ignore[assignment]

    def copy(self) -> dict[K, V]:
        """Return a shallow copy of this :class:`constantdict`."""
        return self.__class__(self)

    # {{{ methods that return a modified copy of the dictionary

    def set(self, key: K, val: V) -> constantdict[K, V]:
        """Return a new :class:`constantdict` with the item at *key* set to *val*."""
        return self.__class__({**self, key: val})

    def delete(self, key: K) -> constantdict[K, V]:
        """Return a new :class:`constantdict` without the item at *key*.

        Raise a :exc:`KeyError` if *key* is not present.
        """
        new = dict(self)
        del new[key]
        return self.__class__(new)

    remove = delete

    def update(self, other: dict[K, V]) -> constantdict[K, V]:  # type: ignore[override]
        """Return a new :class:`constantdict` with updated items from *other*.

        .. note::

            In contrast to :meth:`dict.update`, this method does not modify the
            original :class:`constantdict`, but creates a new, updated copy.
        """
        return self.__class__({**self, **other})

    def discard(self, key: K) -> constantdict[K, V]:
        """Return a new :class:`constantdict` without the item at the given key.

        Return a reference to itself if the key is not present.
        """
        # Based on the pyrsistent.PMap API
        if key not in self:
            return self

        return self.delete(key)

    # }}}

    # {{{ deleted methods

    __delitem__ = _del_attr
    __setitem__ = _del_attr
    clear = _del_attr
    popitem = _del_attr  # type: ignore[assignment]
    pop = _del_attr  # type: ignore[assignment]
    setdefault = _del_attr  # type: ignore[assignment]

    # }}}
