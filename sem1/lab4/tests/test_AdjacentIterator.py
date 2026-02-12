import unittest
from task2.UndirectedGraph import UndirectedGraph
from task2.iterators.AdjacentIterator import AdjacentIterator
from task2.Exceptions import *

class TestAdjacentIterator(unittest.TestCase):

    def setUp(self):
        self.graph = UndirectedGraph[int]()
        self.v1 = self.graph.add_vertex(1)
        self.v2 = self.graph.add_vertex(2)
        self.v3 = self.graph.add_vertex(3)
        self.graph.add_edge(self.v1, self.v2)
        self.graph.add_edge(self.v1, self.v3)

    def test_forward_iteration(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id)
        neighbors = [next(it).value for _ in range(2)]
        self.assertCountEqual(neighbors, [2, 3])
        with self.assertRaises(StopIteration):
            next(it)

    def test_reverse_iteration(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id, reverse=True)
        rev1 = next(it)
        rev2 = next(it)
       
        self.assertCountEqual({rev1.value, rev2.value}, {2, 3})
        with self.assertRaises(StopIteration):
            next(it)

    def test_prev(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id)
        first = next(it)
        second = next(it)

        self.assertEqual(it.prev().value, second.value)

        self.assertEqual(it.prev().value, first.value)

        with self.assertRaises(StopIteration):
            it.prev()

    def test_remove_normal(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id)
        n1 = next(it) 
        it.remove()    

        self.assertFalse(self.graph.has_edge(self.v1, n1))

        remaining = next(it)
        with self.assertRaises(StopIteration):
            next(it)

    def test_remove_on_start_raises(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id)
        with self.assertRaises(NothingToRemove):
            it.remove()

    def test_remove_const_iterator_raises(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id, const=True)
        next(it)
        with self.assertRaises(ConstIterError):
            it.remove()

    def test_iteration_after_remove(self):
      
        it = AdjacentIterator(self.graph, self.v1.vertex_id)
        first = next(it)
        second = next(it)

        it.remove() 
        self.assertFalse(self.graph.has_edge(self.v1, second))
        self.assertEqual(it.prev().value, first.value)

    def test_full_remove_all_neighbors(self):
        it = AdjacentIterator(self.graph, self.v1.vertex_id)
        n1 = next(it)
        it.remove()
        n2 = next(it)
        it.remove()

    
        self.assertEqual(self.graph.vertex_degree(self.v1), 0)

        with self.assertRaises(StopIteration):
            next(it)


