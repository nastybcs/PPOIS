import unittest
from io import StringIO
import sys
from CantorovoSet import CantorovoSet

class TestSet(unittest.TestCase):
    def setUp(self):
        self.s1 = CantorovoSet("{a,b,c}")
        self.s2 = CantorovoSet("{b,c,d}")
        self.empty_set = CantorovoSet("{}")

    def test_initialization(self):
        self.assertEqual(self.s1.get_size(), 3)
        self.assertEqual(self.empty_set.get_size(), 1)  

    def test_add_element(self):
        self.s1.add_element("{d,e}")
        self.assertTrue(self.s1.__getitem__("{d}"))
        self.assertTrue(self.s1.__getitem__("{e}"))
        self.s1.add_element("{a}")
        count_a = sum(1 for el in self.s1.elements if el == ["a"])
        self.assertEqual(count_a, 1)

    def test_remove_element(self):
        self.s1.remove_element("{a}")
        self.assertFalse(self.s1.__getitem__("{a}"))
        self.s1.remove_element("{z}")
        self.assertEqual(self.s1.get_size(), 2)

    def test_union_addition(self):
        s3 = self.s1 + self.s2
        self.assertTrue(s3.__getitem__("{a}"))
        self.assertTrue(s3.__getitem__("{d}"))

    def test_inplace_addition(self):
        self.s1 += self.s2
        self.assertTrue(self.s1.__getitem__("{d}"))
        self.assertEqual(self.s1.get_size(), 4)

    def test_intersection(self):
        s3 = self.s1 * self.s2
        self.assertTrue(s3.__getitem__("{b}"))
        self.assertFalse(s3.__getitem__("{a}"))

    def test_inplace_intersection(self):
        self.s1 *= self.s2
        self.assertFalse(self.s1.__getitem__("{a}"))
        self.assertTrue(self.s1.__getitem__("{b}"))

    def test_difference(self):
        s3 = self.s1 - self.s2
        self.assertTrue(s3.__getitem__("{a}"))
        self.assertFalse(s3.__getitem__("{b}"))

    def test_inplace_difference(self):
        self.s1 -= self.s2
        self.assertFalse(self.s1.__getitem__("{b}"))
        self.assertTrue(self.s1.__getitem__("{a}"))

    def test_boolean(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.s1.boolean()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("{", output)
        self.assertIn("Булеан множества", output)

    def test_cantorovo_algorithm(self):
        elems = [["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"]]
        result = self.s1.cantorovo_algorithm(elems)
        self.assertTrue(len(result) < len(elems))
        self.assertTrue(all(el in elems for el in result))

    def test_getitem(self):
        self.assertTrue(self.s1.__getitem__("{a}"))
        self.assertFalse(self.s1.__getitem__("{z}"))
        self.assertTrue(self.empty_set.__getitem__("{}"))

    def test_print_set_output(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.s1.print_set()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertTrue(output.startswith("{") and output.endswith("}\n"))
        self.assertIn("a", output)

