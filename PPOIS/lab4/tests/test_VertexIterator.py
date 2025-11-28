import unittest
from task2.UndirectedGraph import UndirectedGraph
from task2.iterators.VertexIterator import VertexIterator
from task2.Exceptions import *

class TestVertexIteratorDirect(unittest.TestCase):

    def setUp(self):
        self.graph = UndirectedGraph()
        self.v1 = self.graph.add_vertex("A")
        self.v2 = self.graph.add_vertex("B")
        self.v3 = self.graph.add_vertex("C")

    def test_direct_iteration_forward(self):
        it = VertexIterator(self.graph, reverse=False, const=False)
        values = [v.value for v in it]
        self.assertCountEqual(values, ["A", "B", "C"])

    def test_direct_iteration_reverse(self):
        it = VertexIterator(self.graph, reverse=True, const=False)
        values = [v.value for v in it]
        self.assertCountEqual(values, ["A", "B", "C"])
        self.assertEqual(values[0], "C")  
    def test_direct_prev_normal(self):
        it = VertexIterator(self.graph)
        next(it)  
        prev_vertex = it.prev()
        self.assertEqual(prev_vertex.value, "A")
        with self.assertRaises(StopIteration):
            it.prev()

    def test_direct_remove_normal(self):
        it = VertexIterator(self.graph)
        v = next(it)
        it.remove()
        self.assertFalse(self.graph.has_vertex(v))
        self.assertEqual(len(self.graph._vertices), 2)

    def test_direct_remove_nothing_to_remove(self):
        it = VertexIterator(self.graph)
        with self.assertRaises(NothingToRemove):
            it.remove()

    def test_direct_remove_const_iterator_raises(self):
        it = VertexIterator(self.graph, const=True)
        next(it)
        with self.assertRaises(ConstIterError):
            it.remove()

