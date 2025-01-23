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
from collections.abc import Iterable
from typing import Any, Dict, Hashable, TypeVar  # <3.9 needs Dict, not dict

K = TypeVar("K", bound=Hashable)
V = TypeVar("V", covariant=True)


def _del_attr(self: Any, *args: Any, **kwargs: Any) -> None:
    """Raise an AttributeError when trying to modify the object."""
    raise AttributeError("object is immutable")


# type-ignore-reason: covariant type incompatible with Dict
class constantdict(Dict[K, V]):  # type: ignore[type-var]
    """An immutable dictionary that does not allow modifications after
    creation. This class behaves mostly like a :class:`dict`,
    but with the following differences.

    Additional methods compared to :class:`dict`:

    .. automethod:: __hash__
    .. automethod:: mutate

    Methods that return a modified copy of the :class:`constantdict`:

    .. automethod:: set
    .. automethod:: setdefault
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
    """

    @staticmethod
    def fromkeys(iterable: Iterable[K],  # type: ignore[override]
                 value: V | None = None) -> constantdict[K, V | Any]:
        """Create a new :class:`constantdict` from supplied keys and values."""
        # dict.fromkeys calls __setitem__, hence can't use that directly
        d = constantdictmutation.fromkeys(iterable, value)
        d.__class__ = constantdict
        return d  # type: ignore[return-value]

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

        # Like frozenset.__ior__, constantdict.__ior__ must return a new instance,
        # i.e., augmented assignment instead of in-place modification.
        __ior__ = __or__  # type: ignore[assignment]

    def copy(self) -> dict[K, V]:
        """Return a shallow copy of this :class:`constantdict`."""
        return self.__class__(self)

    # {{{ methods that return a modified copy of the dictionary

    # value: Any due to https://github.com/python/mypy/issues/7049
    def set(self, key: K, value: Any) -> constantdict[K, V]:
        """Return a new :class:`constantdict` with the item at *key* set to *val*."""
        d = self.mutate()
        d[key] = value
        return d.finish()

    def setdefault(self, key: K, default: V | None = None) -> constantdict[K, V]:  # type: ignore[override]
        """Return a new :class:`constantdict` with the item at *key* set to
        *default* if *key* is not in the dictionary.

        Return a reference to itself if *key* is present.

        .. note::

                Based on the frozendict API.
        """
        if key in self:
            return self

        return self.set(key, default)

    def delete(self, key: K) -> constantdict[K, V]:
        """Return a new :class:`constantdict` without the item at *key*.

        Raise a :exc:`KeyError` if *key* is not present.
        """
        d = self.mutate()
        del d[key]
        return d.finish()

    remove = delete

    def update(self, other: dict[K, V]) -> constantdict[K, V]:  # type: ignore[override]
        """Return a new :class:`constantdict` with updated items from *other*.

        .. note::

            In contrast to :meth:`dict.update`, this method does not modify the
            original :class:`constantdict`, but creates a new, updated copy.

        .. doctest::

            >>> cd = constantdict(a=1, b=2)
            >>> cd_new = cd.update({"a": 10, "c": 3})
            >>> cd_new
            constantdict({'a': 10, 'b': 2, 'c': 3})
            >>> cd
            constantdict({'a': 1, 'b': 2})
        """
        d = self.mutate()
        d.update(other)
        return d.finish()

    def discard(self, key: K) -> constantdict[K, V]:
        """Return a new :class:`constantdict` without the item at the given key.

        Return a reference to itself if the key is not present.

        .. note::

            Based on the :class:`pyrsistent.PMap` API.
        """
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

    # }}}

    # {{{ mutation

    def mutate(self) -> constantdictmutation[K, V]:
        """Return a mutable copy of this :class:`constantdict` as a
        :class:`constantdictmutation`.

        Run :meth:`constantdictmutation.finish` to convert back to an immutable
        :class:`constantdict`.

        .. note::

            Based on the `immutables.Map API <https://github.com/MagicStack/immutables>`__.

        .. doctest::

            >>> cd = constantdict(a=1, b=2)
            >>> cd_mut = cd.mutate()
            >>> cd_mut["a"] = 10
            >>> del cd_mut["b"]
            >>> cd_new = cd_mut.finish()
            >>> cd_new
            constantdict({'a': 10})
            >>> cd  # unchanged
            constantdict({'a': 1, 'b': 2})
        """
        # This needs to make a copy since the original dictionary must
        # not be modified.
        return constantdictmutation(self)

    # }}}


# type-ignore-reason: covariant type incompatible with Dict
class constantdictmutation(Dict[K, V]):  # type: ignore[type-var]
    """A mutable dictionary that can be converted back to a
    :class:`constantdict` without copying. This class behaves exactly like a
    :class:`dict`, except for one additional method mentioned below.

    Additional method compared to :class:`dict`:

    .. automethod:: finish
    """

    def finish(self) -> constantdict[K, V]:
        """Convert this object to an immutable version of itself.

        .. doctest::

            >>> cd_mut = constantdict(a=1, b=2).mutate()
            >>> cd_mut["a"] = 12
            >>> cd = cd_mut.finish()
            >>> cd
            constantdict({'a': 12, 'b': 2})
        """
        self.__class__ = constantdict  # type: ignore[assignment]
        return self  # type: ignore[return-value]


class constantdictuncachedhash(constantdict[K, V]):
    """A :class:`constantdict` that does not cache its hash
    value. This is useful when the dictionary contains items that are not
    immutable and whose hash value might therefore change.

    .. automethod:: mutate
    """

    def __hash__(self) -> int:  # type: ignore[override]
        # Same "algorithm" as in constantdict
        return hash(frozenset(self.items()))

    def mutate(self) -> constantdictuncachedhashmutation[K, V]:
        """Return a mutable copy of this :class:`constantdict` as a
        :class:`constantdictuncachedhashmutation`.

        Run :meth:`constantdictuncachedhashmutation.finish` to convert back to an
        immutable :class:`constantdict`.
        """
        return constantdictuncachedhashmutation(self)


class constantdictuncachedhashmutation(constantdictmutation[K, V]):
    """A mutable dictionary that can be converted back to a
    :class:`constantdictuncachedhash` without copying. This class behaves
    exactly like a :class:`dict`, except for one additional method mentioned
    below.

    Additional method compared to :class:`dict`:

    .. automethod:: finish
    """

    def finish(self) -> constantdictuncachedhash[K, V]:
        """Convert this object to an immutable version of itself."""
        self.__class__ = constantdictuncachedhash  # type: ignore[assignment]
        return self  # type: ignore[return-value]
