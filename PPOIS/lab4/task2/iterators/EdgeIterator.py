from task2.Exceptions import *
from task2.Edge import Edge
class EdgeIterator:
    def __init__(self, graph, reverse=False, const=False):
        self.graph = graph
        edges = []

        for first_vertex in graph._adj:
            for second_vertex in graph._adj[first_vertex]:
                if first_vertex < second_vertex: 
                    edges.append((first_vertex, second_vertex))

        if reverse:
            edges.reverse()

        self.edges = edges
        self.index = 0
        self.const = const

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.edges):
            raise StopIteration
        first_vertex_id, second_vertex_id = self.edges[self.index]
        self.index += 1
        first_vertex = self.graph._vertices[first_vertex_id]
        second_vertex = self.graph._vertices[second_vertex_id]
        return Edge(first_vertex, second_vertex)

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        u_id, v_id = self.edges[self.index]
        return Edge(self.graph._vertices[u_id], self.graph._vertices[v_id])


    def remove(self):
        if self.const:
            raise ConstIterError("Константный итератор не может удалять элемент")
        if self.index == 0:
            raise NothingToRemove("Нечего удалять")
        first_vertex_id, second_vertex_id = self.edges[self.index - 1]
        first_vertex_obj = self.graph._vertices[first_vertex_id]
        second_vertex_obj = self.graph._vertices[second_vertex_id]
        self.graph.remove_edge(first_vertex_obj, second_vertex_obj)
        del self.edges[self.index - 1]
        self.index -= 1
        