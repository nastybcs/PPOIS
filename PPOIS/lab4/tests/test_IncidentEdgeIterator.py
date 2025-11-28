import unittest
from task2.UndirectedGraph import UndirectedGraph
from task2.iterators.IncidentEdgeIterator import IncidentEdgeIterator
from task2.Exceptions import *


class TestIncidentEdgeIterator(unittest.TestCase):

    def setUp(self):
        self.graph = UndirectedGraph()
        self.v1 = self.graph.add_vertex(1)
        self.v2 = self.graph.add_vertex(2)
        self.v3 = self.graph.add_vertex(3)

        self.graph.add_edge(self.v1, self.v2)
        self.graph.add_edge(self.v1, self.v3)

    def test_iteration_normal(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id)
        edges = list(it)

        vals = sorted([(e.first_vertex.value, e.second_vertex.value) for e in edges])
        self.assertEqual(vals, [(1, 2), (1, 3)])

    def test_iteration_reverse(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id, reverse=True)
        edges = list(it)

        vals = [(e.first_vertex.value, e.second_vertex.value) for e in edges]
        self.assertEqual(vals, [(1, 3), (1, 2)])

    def test_prev(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id)
        _ = next(it)
        back = it.prev()

        self.assertIn(
            (back.first_vertex.value, back.second_vertex.value),
            [(1, 2), (1, 3)]
        )

    def test_prev_raises_at_start(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id)
        with self.assertRaises(StopIteration):
            it.prev()

    def test_remove_normal(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id)
        first = next(it)
        it.remove()

        self.assertFalse(self.graph.has_edge(first.first_vertex, first.second_vertex))
        self.assertEqual(len(it.edges), 1)

    def test_remove_const_iterator_raises(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id, const=True)
        next(it)
        with self.assertRaises(ConstIterError):
            it.remove()

    def test_remove_nothing_to_remove(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id)
        with self.assertRaises(NothingToRemove):
            it.remove()

    def test_remove_index_consistency(self):
        it = IncidentEdgeIterator(self.graph, self.v1.vertex_id)
        e1 = next(it)
        e2 = next(it)

        it.remove()  

        back = it.prev()
        self.assertEqual(
            (back.first_vertex.value, back.second_vertex.value),
            (1, 2)
        )
