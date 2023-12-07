from typing import Generic, TypeVar

T = TypeVar('T')


class Pointer(Generic[T]):
    def __init__(self, v: T) -> None:
        self._val = v
    
    def set(self, v: T):
        self._val = v
    
    def get(self):
        return self._val

    def __lshift__(self, v):
        self.set(v)
    
    def __pos__(self):
        return self.get()
