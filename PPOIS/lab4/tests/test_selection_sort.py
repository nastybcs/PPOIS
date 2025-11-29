import unittest
from task1.selection_sort import SelectionSort
from task1.Item import Item


class TestSelectionSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(SelectionSort.selection_sort([]), [])

    def test_single_element(self):
        self.assertEqual(SelectionSort.selection_sort([5]), [5])

    def test_numbers_ascending(self):
        self.assertEqual(SelectionSort.selection_sort([3, 1, 4, 1, 5]), [1, 1, 3, 4, 5])

    def test_numbers_with_key(self):
        items = [Item(3), Item(1), Item(4)]
        sorted_items = SelectionSort.selection_sort(items, key=lambda x: x.value)
        self.assertEqual(sorted_items, [Item(1), Item(3), Item(4)])

    def test_does_not_mutate_original(self):
        original = [3, 1, 2]
        copy = original[:]
        SelectionSort.selection_sort(original)
        self.assertEqual(original, copy)  