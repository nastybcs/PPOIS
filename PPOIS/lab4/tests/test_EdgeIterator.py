import unittest
from task2.UndirectedGraph import UndirectedGraph
from task2.iterators.EdgeIterator import EdgeIterator
from task2.Exceptions import *
from task2.Edge import Edge


class TestEdgeIterator(unittest.TestCase):

    def setUp(self):
        self.graph = UndirectedGraph[int]()
        self.v1 = self.graph.add_vertex(1)
        self.v2 = self.graph.add_vertex(2)
        self.v3 = self.graph.add_vertex(3)

        self.graph.add_edge(self.v1, self.v2)
        self.graph.add_edge(self.v1, self.v3)

    def test_forward_iteration(self):
        it = EdgeIterator(self.graph)
        edges = []

        for e in it:
            edges.append((e.first_vertex.value, e.second_vertex.value))

        self.assertEqual(len(edges), 2)
        self.assertCountEqual(edges, [(1, 2), (1, 3)])

        with self.assertRaises(StopIteration):
            next(it)

    def test_reverse_iteration(self):
        it = EdgeIterator(self.graph, reverse=True)
        edges = [next(it), next(it)]

        values = {(e.first_vertex.value, e.second_vertex.value) for e in edges}
        self.assertEqual(len(values), 2)
        self.assertIn((1, 2), values)
        self.assertIn((1, 3), values)

        with self.assertRaises(StopIteration):
            next(it)

    def test_prev(self):
        it = EdgeIterator(self.graph)
        e1 = next(it)
        e2 = next(it)

        back1 = it.prev()
        self.assertEqual((back1.first_vertex.value, back1.second_vertex.value),
                         (e2.first_vertex.value, e2.second_vertex.value))

        back2 = it.prev()
        self.assertEqual((back2.first_vertex.value, back2.second_vertex.value),
                         (e1.first_vertex.value, e1.second_vertex.value))

        with self.assertRaises(StopIteration):
            it.prev()


    def test_remove_normal(self):
        it = EdgeIterator(self.graph)
        e1 = next(it)  
        it.remove()    

        self.assertFalse(self.graph.has_edge(e1.first_vertex, e1.second_vertex))

        e2 = next(it)
        self.assertTrue(self.graph.has_edge(e2.first_vertex, e2.second_vertex))

        with self.assertRaises(StopIteration):
            next(it)

    def test_remove_at_start_raises(self):
        it = EdgeIterator(self.graph)
        with self.assertRaises(NothingToRemove):
            it.remove()

    def test_remove_const_iterator_raises(self):
        it = EdgeIterator(self.graph, const=True)
        next(it)
        with self.assertRaises(ConstIterError):
            it.remove()

    def test_remove_and_prev_consistency(self):
        it = EdgeIterator(self.graph)
        e1 = next(it)
        e2 = next(it)

        it.remove()  

        back = it.prev()
        self.assertEqual((back.first_vertex.value, back.second_vertex.value),
                         (e1.first_vertex.value, e1.second_vertex.value))


    def test_remove_all_edges(self):
        it = EdgeIterator(self.graph)

        e1 = next(it)
        it.remove()

        e2 = next(it)
        it.remove()


        self.assertEqual(self.graph.edge_count(), 0)

        with self.assertRaises(StopIteration):
            next(it)


