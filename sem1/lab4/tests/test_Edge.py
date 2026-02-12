import unittest
from task2.Edge import Edge
from task2.Vertex import Vertex
from task2.Exceptions import EdgeHaveNotVertexError

class TestEdge(unittest.TestCase):

    def setUp(self):
        self.v1 = Vertex(1, "A")
        self.v2 = Vertex(2, "B")
        self.v3 = Vertex(3, "C")

    def test_edge_properties(self):
        edge = Edge(self.v1, self.v2)
        self.assertIs(edge.first_vertex, self.v1)
        self.assertIs(edge.second_vertex, self.v2)

    def test_edge_eq(self):
        edge1 = Edge(self.v1, self.v2)
        edge2 = Edge(self.v2, self.v1)
        edge3 = Edge(self.v1, self.v3)

        self.assertEqual(edge1, edge2)  
        self.assertNotEqual(edge1, edge3)

    def test_other_vertex(self):
        edge = Edge(self.v1, self.v2)
        self.assertIs(edge.other(self.v1), self.v2)
        self.assertIs(edge.other(self.v2), self.v1)

       
        with self.assertRaises(EdgeHaveNotVertexError):
            edge.other(self.v3)

    def test_repr(self):
        edge = Edge(self.v1, self.v2)
        self.assertEqual(repr(edge), "Edge(1-2)")
