class Pointer:
    def __init__(self, v) -> None:
        self._val = v
    
    def set(self, v):
        self._val = v
    
    def get(self):
        return self._val

    def __lshift__(self, v):
        self.set(v)
    
    def __pos__(self):
        return self.get()
