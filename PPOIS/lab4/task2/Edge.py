from task2.Vertex import Vertex
from task2.Exceptions import EdgeHaveNotVertexError
class Edge[T]:
    def __init__(self, first_vertex: Vertex, second_vertex: Vertex):
        self._first_vertex = first_vertex
        self._second_vertex = second_vertex

    @property
    def first_vertex(self):
        return self._first_vertex
    
    @property
    def second_vertex(self):
        return self._second_vertex
    
    def __eq__(self,other):
        if not isinstance(other, Edge):
            return False
        return {self._first_vertex.vertex_id, self._second_vertex.vertex_id} == \
               {other._first_vertex.vertex_id, other._second_vertex.vertex_id}
    
    def other(self, vertex: Vertex[T]) -> Vertex[T]:
        if vertex.vertex_id == self._first_vertex.vertex_id:
            return self._second_vertex
        if vertex.vertex_id == self._second_vertex.vertex_id:
            return self._first_vertex
        raise EdgeHaveNotVertexError("Вершина не принадлежит ребру")
    
    def __repr__(self):
        return f"Edge({self._first_vertex.vertex_id}-{self._second_vertex.vertex_id})"