from task2.Edge import Edge
from task2.Exceptions import *
from task2.Edge import Edge
from task2.Exceptions import *

class IncidentEdgeIterator:
    def __init__(self, graph, vertex_id, reverse=False, const=False):
        self.graph = graph
        self.vertex_id = vertex_id

        edges = [(min(vertex_id, x), max(vertex_id, x)) for x in graph._adj[vertex_id]]
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
        first_id, second_id = self.edges[self.index]
        self.index += 1

        return Edge(self.graph._vertices[first_id],
                    self.graph._vertices[second_id])

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        first_id, second_id = self.edges[self.index]
        return Edge(self.graph._vertices[first_id],
                    self.graph._vertices[second_id])

    def remove(self):
        if self.const:
            raise ConstIterError("Константный итератор не может удалять элемент")

        if self.index == 0:
            raise NothingToRemove("Нечего удалять")

        first_id, second_id = self.edges[self.index - 1]

        v1 = self.graph._vertices[first_id]
        v2 = self.graph._vertices[second_id]

        self.graph.remove_edge(v1, v2)

        del self.edges[self.index - 1]
        self.index -= 1
