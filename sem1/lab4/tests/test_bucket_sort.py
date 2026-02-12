import unittest
from task1.bucket_sort import BucketSort
from task1.Item import Item
class TestBucketSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(BucketSort.bucket_sort([]), [])

    def test_single_element(self):
        self.assertEqual(BucketSort.bucket_sort([42]), [42])

    def test_numbers_default_key(self):
        self.assertEqual(BucketSort.bucket_sort([9, 1, 5, 3, 9, 2]), [1, 2, 3, 5, 9, 9])

    def test_numbers_with_duplicates(self):
        self.assertEqual(BucketSort.bucket_sort([2, 2, 2, 1, 3]), [1, 2, 2, 2, 3])

    def test_all_elements_equal(self):
        self.assertEqual(BucketSort.bucket_sort([7, 7, 7]), [7, 7, 7])

    def test_item_objects(self):
        items = [Item(5), Item(1), Item(9), Item(3), Item(7)]
        result = BucketSort.bucket_sort(items, key=lambda x: x.value)
        self.assertEqual([i.value for i in result], [1, 3, 5, 7, 9])

    def test_tuples_by_first_element(self):
        data = [(3, 'c'), (1, 'a'), (2, 'b'), (4, 'd')]
        result = BucketSort.bucket_sort(data, key=lambda x: x[0])
        self.assertEqual(result, [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')])

    def test_lists_by_length(self):
        data = [[1, 2], [1], [1, 2, 3], []]
        result = BucketSort.bucket_sort(data, key=len)
        self.assertEqual([len(lst) for lst in result], [0, 1, 2, 3])

    def test_does_not_mutate_original(self):
        original = [Item(5), Item(1), Item(9)]
        copy = [i.value for i in original]
        BucketSort.bucket_sort(original, key=lambda x: x.value)
        self.assertEqual([i.value for i in original], copy)

    def test_float_values(self):
        self.assertEqual(
            BucketSort.bucket_sort([3.5, 1.1, 4.4, 2.2]),
            [1.1, 2.2, 3.5, 4.4]
        )

    def test_negative_numbers(self):
        self.assertEqual(
            BucketSort.bucket_sort([-5, -1, -9, 0, -3]),
            [-9, -5, -3, -1, 0]
        )
