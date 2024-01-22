from __future__ import annotations

__copyright__ = """
Copyright (C) 2023 University of Illinois Board of Trustees
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


from typing import Any, Mapping, Type, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def _del_attr(self: Any, *args: Any, **kwargs: Any) -> None:
    """Raise an AttributeError when trying to modify the object."""
    raise AttributeError("object is immutable")


class constantdict(dict[K, V]):  # noqa: N801
    @classmethod
    def fromkeys(_cls: Type[Mapping[K, V]], *args: Any,  # type: ignore[override]
                 **kwargs: Any) -> Mapping[K, V]:
        # dict.fromkeys calls __setitem__, hence need to convert
        return _cls(dict.fromkeys(*args, **kwargs))

    def __hash__(self) -> int:  # type: ignore[override]
        try:
            return self._hash  # type: ignore[has-type,no-any-return]
        except AttributeError:
            h = 0
            for key, value in self.items():
                h ^= hash((key, value))
            self._hash = h
            return h

    __delitem__ = _del_attr
    __setitem__ = _del_attr
    clear = _del_attr
    popitem = _del_attr  # type: ignore[assignment]
    pop = _del_attr  # type: ignore[assignment]
    setdefault = _del_attr  # type: ignore[assignment]
    update = _del_attr
