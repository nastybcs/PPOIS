from task2.Exceptions import *
class VertexIterator:
    def __init__(self, graph, reverse=False, const=False):
        self.graph = graph
        self.vertices = list(graph._adj.keys())
        if reverse:
            self.vertices.reverse()
        self.index = 0
        self.const = const

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.vertices):
            raise StopIteration
        vertex_id = self.vertices[self.index]
        self.index += 1
        return self.graph._vertices[vertex_id]

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        vertex_id = self.vertices[self.index]
        return self.graph._vertices[vertex_id]

    def remove(self):
        if self.const:
            raise ConstIterError("Константный итератор не может удалять элемент")

        if self.index == 0:
            raise NothingToRemove("Нечего удалять")

        vertex_id = self.vertices[self.index - 1]
        vertex_obj = self.graph._vertices[vertex_id]
        self.graph.remove_vertex(vertex_obj)
        del self.vertices[self.index - 1]
        self.index -= 1