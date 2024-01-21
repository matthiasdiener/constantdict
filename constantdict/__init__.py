from typing import Any



def _del_attr(*args, **kwargs):
    raise AttributeError("object is immutable")


class constantdict(dict):
    def __new__(cls, *args: Any, **kwargs: Any):
        inst = super().__new__(cls)
        setattr(inst, "_hash", None)
        return inst

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        return cls(dict.fromkeys(*args, **kwargs))

    def __setitem__(self, key, value) -> None:
        _del_attr()

    def __delitem__(self, key) -> None:
        _del_attr()

    def clear(self) -> None:
        _del_attr()

    def popitem(self) -> None:
        _del_attr()

    def update(self, *args, **kwargs) -> None:
        _del_attr()

    def __hash__(self) -> int:
        if self._hash is None:
            h = 0
            for key, value in self.items():
                h ^= hash((key, value))
            self._hash = h

        return self._hash

