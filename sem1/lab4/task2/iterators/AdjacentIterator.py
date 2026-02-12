from task2.Exceptions import *
class AdjacentIterator:
    def __init__(self, graph, vertex_id, reverse=False, const=False):
        self.graph = graph
        self.vertex_id = vertex_id
        adj = list(graph._adj[vertex_id])
        if reverse:
            adj.reverse()
        self.adj = adj
        self.index = 0
        self.const = const

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.adj):
            raise StopIteration
        neighbor_id = self.adj[self.index]
        self.index += 1
        return self.graph._vertices[neighbor_id]

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        neighbor_id = self.adj[self.index]
        return self.graph._vertices[neighbor_id]

    def remove(self):
        if self.const:
            raise ConstIterError("Константный итератор не может удалять элемент")
        if self.index == 0:
            raise NothingToRemove("Нечего удалять")
        neighbor_id = self.adj[self.index - 1]
        first_vertex = self.graph._vertices[self.vertex_id]
        second_vertex = self.graph._vertices[neighbor_id]
        self.graph.remove_edge(first_vertex, second_vertex)
        del self.adj[self.index - 1]
        self.index -= 1
