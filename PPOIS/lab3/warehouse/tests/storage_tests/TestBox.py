
import unittest
from storage.box import Box
from storage.bin import Bin
from storage.batch import Batch
from core.product import Product
from enums.bin_type import BinType
from enums.product_category import Category
from exceptions.errors import WarehouseError


class TestBox(unittest.TestCase):

    def setUp(self):
        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")
        self.batch = Batch(self.product, "B001", 10)

    def test_init_inherits_from_bin_and_sets_sealed_false(self):
        box = Box("BOX-01")
        self.assertIsInstance(box, Bin)
        self.assertEqual(box.code, "BOX-01")
        self.assertEqual(box.bin_type, BinType.SMALL_BOX)
        self.assertEqual(box.capacity, 50)
        self.assertFalse(box.sealed)

    def test_init_with_custom_type_and_capacity(self):
        box = Box("BIG-01", BinType.LARGE_PALLET, capacity=1000)
        self.assertEqual(box.bin_type, BinType.LARGE_PALLET)
        self.assertEqual(box.capacity, 1000)


    def test_seal_sets_sealed_true_and_changes_bin_type(self):
        box = Box("BOX-01")
        box.seal()
        self.assertTrue(box.sealed)
        self.assertEqual(box.bin_type, BinType.SEALED_BOX)

    def test_seal_raises_error_if_already_sealed(self):
        box = Box("BOX-01")
        box.seal()
        with self.assertRaises(WarehouseError) as cm:
            box.seal()
        self.assertIn("уже запечатана", str(cm.exception))



    def test_receive_batch_works_when_not_sealed(self):
        box = Box("BOX-01", capacity=100)
        box.receive_batch(self.batch)
        self.assertEqual(box.total_qty("P001"), 10)
        self.assertEqual(box.current_load, 10)

    def test_receive_batch_raises_error_if_sealed(self):
        box = Box("BOX-01", capacity=100)
        box.seal()
        with self.assertRaises(WarehouseError) as cm:
            box.receive_batch(self.batch)
        self.assertIn("Нельзя добавить в запечатанную коробку", str(cm.exception))

    def test_receive_batch_calls_super_when_not_sealed(self):
        box = Box("BOX-01", capacity=100)
        box.receive_batch(self.batch)
        self.assertIn("P001", box.storage)
        self.assertEqual(len(box.storage["P001"]), 1)

