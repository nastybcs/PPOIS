class Vertex[T]:
    def __init__(self, vertex_id: int, value: T):
        self._vertex_id = vertex_id
        self._value = value

    @property
    def value(self):
        return self._value
    
    @property
    def vertex_id(self):
        return self._vertex_id
    
    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return self.vertex_id == other.vertex_id
    def __repr__(self):
        return f"Vertex(id={self._vertex_id}, val={self._value!r})"
    
    
