import unittest
from task2.Vertex import Vertex

class TestVertex(unittest.TestCase):

    def test_vertex_creation(self):
        v = Vertex(1, "A")
        self.assertEqual(v.vertex_id, 1)
        self.assertEqual(v.value, "A")

    def test_vertex_eq(self):
        v1 = Vertex(1, "A")
        v2 = Vertex(1, "B") 
        v3 = Vertex(2, "A")

        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)
        self.assertNotEqual(v1, "not a vertex")  

    def test_vertex_repr(self):
        v = Vertex(1, "A")
        self.assertEqual(repr(v), "Vertex(id=1, val='A')")

