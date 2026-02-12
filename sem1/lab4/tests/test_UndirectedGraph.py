import unittest
from task2.UndirectedGraph import UndirectedGraph
from task2.Vertex import Vertex
from task2.Edge import Edge
from task2.Exceptions import *

class TestUndirectedGraphFull(unittest.TestCase):

    def setUp(self):
        self.graph = UndirectedGraph()
        self.v1 = self.graph.add_vertex(10)
        self.v2 = self.graph.add_vertex(20)
        self.v3 = self.graph.add_vertex(30)

        self.e1 = self.graph.add_edge(self.v1, self.v2)
        self.e2 = self.graph.add_edge(self.v1, self.v3)

    def test_empty_clear(self):
        g = UndirectedGraph()
        self.assertTrue(g.empty())
        g.add_vertex(5)
        self.assertFalse(g.empty())
        g.clear()
        self.assertTrue(g.empty())
        self.assertEqual(g.vertex_count(), 0)
        self.assertEqual(g.edge_count(), 0)

    def test_vertex_count_edge_count(self):
        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertEqual(self.graph.edge_count(), 2)

    def test_add_vertex_edge_and_has_methods(self):
        v = self.graph.add_vertex(40)
        self.assertTrue(self.graph.has_vertex(v))

        e = self.graph.add_edge(v, self.v1)
        self.assertTrue(self.graph.has_edge(v, self.v1))
        self.assertTrue(self.graph.has_edge(self.v1, v))

    def test_vertex_degree_edge_degree(self):
        deg = self.graph.vertex_degree(self.v1)
        self.assertEqual(deg, 2)
        edge_deg = self.graph.edge_degree(self.e1)
        self.assertEqual(edge_deg, 3)  
    def test_remove_vertex(self):
        self.graph.remove_vertex(self.v2)
        self.assertFalse(self.graph.has_vertex(self.v2))
        self.assertEqual(self.graph.vertex_count(), 2)
        self.assertEqual(self.graph.edge_count(), 1)

    def test_remove_edge(self):
        self.graph.remove_edge(self.v1, self.v2)
        self.assertFalse(self.graph.has_edge(self.v1, self.v2))
        self.assertEqual(self.graph.edge_count(), 1)

    def test_copy_and_iadd(self):
        g2 = self.graph.copy()
        self.assertEqual(g2.vertex_count(), 3)
        self.assertEqual(g2.edge_count(), 2)

        g2 += self.graph
        self.assertEqual(g2.vertex_count(), 6)
   
        self.assertEqual(g2.edge_count(), 2)

    def test_eq_ne(self):
        g2 = self.graph.copy()
        self.assertTrue(self.graph == g2)
        self.assertFalse(self.graph != g2)
        g2.add_vertex(50)
        self.assertFalse(self.graph == g2)
        self.assertTrue(self.graph != g2)

    def test_comparison(self):
        g2 = self.graph.copy()
        g2.add_vertex(50)
        self.assertTrue(self.graph < g2)
        self.assertTrue(self.graph <= g2)
        self.assertFalse(self.graph > g2)
        self.assertFalse(self.graph >= g2)

    def test_str_repr(self):
        s = str(self.graph)
        self.assertIn("Vertices:", s)
        self.assertIn("Edges:", s)
        r = repr(self.graph)
        self.assertIn("UndirectedGraph", r)

    def test_iterators(self):
        ids = [v.vertex_id for v in self.graph.begin()]
        self.assertEqual(set(ids), {self.v1.vertex_id, self.v2.vertex_id, self.v3.vertex_id})

        rev_ids = [v.vertex_id for v in self.graph.rbegin()]
        self.assertEqual(set(rev_ids), {self.v1.vertex_id, self.v2.vertex_id, self.v3.vertex_id})
  
        const_ids = [v.vertex_id for v in self.graph.cbegin()]
        self.assertEqual(set(const_ids), {self.v1.vertex_id, self.v2.vertex_id, self.v3.vertex_id})

    def test_exceptions(self):
        g = UndirectedGraph()
        v = Vertex(0, 10)
        with self.assertRaises(GraphHaveNotVertex):
            g.has_edge(v, v)
        with self.assertRaises(GraphHaveNotVertex):
            g.add_edge(v, v)
        with self.assertRaises(GraphHaveNotVertex):
            g.vertex_degree(v)
        with self.assertRaises(GraphHaveNotVertex):
            g.edge_degree(Edge(v, v))
        with self.assertRaises(GraphHaveNotVertex):
            g.remove_vertex(v)
        with self.assertRaises(GraphHaveNotVertex):
            g.remove_edge(v, v)

    def test_self_loop_edge(self):
        loop = self.graph.add_edge(self.v1, self.v1)
        self.assertTrue(self.graph.has_edge(self.v1, self.v1))
        self.assertEqual(self.graph.vertex_degree(self.v1), 4)
        self.graph.remove_edge(self.v1, self.v1)
        self.assertFalse(self.graph.has_edge(self.v1, self.v1))
