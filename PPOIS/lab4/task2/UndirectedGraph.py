from task2.Vertex import Vertex
from task2.Edge import Edge
from copy import deepcopy
from task2.Exceptions import *
from task2.iterators.VertexIterator import VertexIterator

class UndirectedGraph[T]:

    def __init__(self):
        self._vertices: dict[int, Vertex[T]] = {}
        self._adj: dict[int, set[int]] = {}
        self._next_id = 0

    def empty(self) -> bool:
        return len(self._vertices) == 0 

    def clear(self) -> None:
        self._vertices.clear()
        self._adj.clear()
        self._next_id = 0

    def __deepcopy__(self, memo):
        new_graph = UndirectedGraph[T]()
        new_graph._vertices = {vid: Vertex(vid, deepcopy(vertex.value, memo)) 
                             for vid, vertex in self._vertices.items()}
        new_graph._adj = {k: v.copy() for k, v in self._adj.items()}
        new_graph._next_id = self._next_id
        return new_graph
    
    def copy(self):
        return self.__deepcopy__({})
    
    def __iadd__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        
        for vertex in other._vertices.values():
            self.add_vertex(deepcopy(vertex.value))
        
        for vertex_id, neighbors in other._adj.items():
            for neighbor_id in neighbors:
                if vertex_id < neighbor_id:  
                    v1 = self._vertices[vertex_id]
                    v2 = self._vertices[neighbor_id]
                    self.add_edge(v1, v2)
        return self
    
    def __eq__(self, other):
        if not isinstance(other, UndirectedGraph):
            return False
        
        if len(self._vertices) != len(other._vertices):
            return False
 
        if self.edge_count() != other.edge_count():
            return False
            
        return self._adj == other._adj
    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self.vertex_count() < other.vertex_count()

    def __le__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self.vertex_count() <= other.vertex_count()

    def __gt__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self.vertex_count() > other.vertex_count()

    def __ge__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self.vertex_count() >= other.vertex_count()

    def vertex_count(self) -> int:
        return len(self._vertices)

    
    def __str__(self) -> str:
        parts = ["Vertices:"]
        for vertex in self.begin():  
            parts.append(f"  {vertex.vertex_id}: {vertex.value}")
    
        parts.append("Edges:")
        seen = set()
        for v_id, neighbors in self._adj.items():
            for n_id in neighbors:
                edge = tuple(sorted((v_id, n_id)))
                if edge not in seen:
                    seen.add(edge)
                    parts.append(f"  {edge[0]}-{edge[1]}")
        return "\n".join(parts)

    

    def edge_count(self) -> int:
        total = sum(len(neighbours) for neighbours in self._adj.values())
        loops = sum(1 for vertex_id, neighbours in self._adj.items() 
                    if vertex_id in neighbours)
        return (total + loops) // 2

    def add_vertex(self, value: T) -> Vertex[T]:
        vertex_id = self._next_id
        vertex = Vertex(vertex_id, value)
        self._vertices[vertex_id] = vertex
        self._adj[vertex_id] = set()
        self._next_id += 1
        return vertex

    def add_edge(self,first_vertex: Vertex[T], second_vertex: Vertex[T]) -> Edge[T]:
        if first_vertex.vertex_id not in self._vertices or second_vertex.vertex_id not in self._vertices:
            raise GraphHaveNotVertex("Одна из вершин не принадлежит графу")
        self._adj[first_vertex.vertex_id].add(second_vertex.vertex_id)
        self._adj[second_vertex.vertex_id].add(first_vertex.vertex_id)
        return Edge(first_vertex, second_vertex)
    
    def has_vertex(self,vertex: Vertex[T])-> bool:
        return vertex.vertex_id in self._vertices
    
    def has_edge(self, first_vertex: Vertex[T], second_vertex: Vertex[T]) -> bool:
        if not self.has_vertex(first_vertex) or not self.has_vertex(second_vertex):
            raise GraphHaveNotVertex("Одна из вершин не принадлежит графу")
        return second_vertex.vertex_id in self._adj[first_vertex.vertex_id]

    def vertex_degree(self, vertex: Vertex[T]) -> int:
        if not self.has_vertex(vertex):
            raise GraphHaveNotVertex("Вершина не принадлежит графу")

        degree = 0
        for neighbor_id in self._adj[vertex.vertex_id]:
            if neighbor_id == vertex.vertex_id:
                degree += 2  
            else:
                degree += 1
        return degree

    
    def edge_degree(self, edge: Edge[T]):
        if not self.has_vertex(edge.first_vertex) or not self.has_vertex(edge.second_vertex):
            raise GraphHaveNotVertex("Одна из вершин не принадлежит графу")
        return ((self.vertex_degree(edge.first_vertex))+
                self.vertex_degree(edge.second_vertex))
    
    def remove_vertex(self, vertex: Vertex[T]) -> None:
        if not self.has_vertex(vertex):
            raise GraphHaveNotVertex("Вершина не принадлежит графу")
        vertex_id = vertex.vertex_id
        for neighbour_id in list(self._adj[vertex_id]):
            self._adj[neighbour_id].discard(vertex_id)
        del self._adj[vertex_id]
        del self._vertices[vertex_id]
    
    def remove_edge(self, first_vertex: Vertex[T], second_vertex: Vertex[T]) -> None:
        if not self.has_vertex(first_vertex) or not self.has_vertex(second_vertex):
            raise GraphHaveNotVertex("Одна из вершин не принадлежит графу")
        first_id = first_vertex.vertex_id
        second_id = second_vertex.vertex_id
        self._adj[first_id].discard(second_id)
        self._adj[second_id].discard(first_id)

    def begin(self):
        return VertexIterator(self, reverse=False, const=False)

    def end(self):
        it = VertexIterator(self, reverse=False, const=False)
        it.index = len(it.vertices)
        return it

    def rbegin(self):
        return VertexIterator(self, reverse=True, const=False)

    def rend(self):
        it = VertexIterator(self, reverse=True, const=False)
        it.index = len(it.vertices)
        return it


    def cbegin(self):
        return VertexIterator(self, reverse=False, const=True)

    def cend(self):
        it = VertexIterator(self, reverse=False, const=True)
        it.index = len(it.vertices)
        return it

    def crbegin(self):
        return VertexIterator(self, reverse=True, const=True)

    def crend(self):
        it = VertexIterator(self, reverse=True, const=True)
        it.index = len(it.vertices)
        return it
    

    def __repr__(self):
        return f"UndirectedGraph<{T.__name__}>(vertices={self.vertex_count()}, edges={self.edge_count()})"
