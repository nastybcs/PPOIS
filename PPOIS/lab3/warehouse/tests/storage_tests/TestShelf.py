
import unittest

from core.product import Product
from storage.batch import Batch
from storage.shelf import Shelf
from enums.bin_type import BinType
from enums.product_category import Category
from exceptions.errors import WarehouseError


class TestShelf(unittest.TestCase):

    def setUp(self):
        self.food_product = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")
        self.chem_product = Product("Acid", "P002", 100, 0.5, Category.CHEMICAL, "LITER")
        self.hazard_product = Product("Explosive", "P003", 200, 0.1, Category.HAZARD, "KG")


    def test_init_calls_super_with_correct_args(self):
        shelf = Shelf("FR-01", BinType.FRIDGE, capacity=500)
        self.assertEqual(shelf.code, "FR-01")
        self.assertEqual(shelf.bin_type, BinType.FRIDGE)
        self.assertEqual(shelf.capacity, 500)
        self.assertEqual(shelf.current_load, 0)


    def test_receive_batch_fridge_accepts_food(self):
        shelf = Shelf("FR-01", BinType.FRIDGE)
        batch = Batch(self.food_product, "B001", 100)
        shelf.receive_batch(batch)  
        self.assertEqual(shelf.total_qty("P001"), 100)

    def test_receive_batch_chemical_accepts_chemical(self):
        shelf = Shelf("CH-01", BinType.CHEMICAL)
        batch = Batch(self.chem_product, "B002", 50)
        shelf.receive_batch(batch)
        self.assertEqual(shelf.total_qty("P002"), 50)

    def test_receive_batch_hazard_accepts_hazard(self):
        shelf = Shelf("HZ-01", BinType.HAZARD)
        batch = Batch(self.hazard_product, "B003", 30)
        shelf.receive_batch(batch)
        self.assertEqual(shelf.total_qty("P003"), 30)

   

    def test_receive_batch_fridge_rejects_non_food(self):
        shelf = Shelf("FR-01", BinType.FRIDGE)
        batch = Batch(self.chem_product, "B004", 10)
        with self.assertRaises(WarehouseError) as cm:
            shelf.receive_batch(batch)
        self.assertIn("нельзя в холодильник", str(cm.exception))

    def test_receive_batch_chemical_rejects_non_chemical(self):
        shelf = Shelf("CH-01", BinType.CHEMICAL)
        batch = Batch(self.food_product, "B005", 10)
        with self.assertRaises(WarehouseError) as cm:
            shelf.receive_batch(batch)
        self.assertIn("нельзя на хим. полку", str(cm.exception))

    def test_receive_batch_hazard_rejects_non_hazard(self):
        shelf = Shelf("HZ-01", BinType.HAZARD)
        batch = Batch(self.food_product, "B006", 10)
        with self.assertRaises(WarehouseError) as cm:
            shelf.receive_batch(batch)
        self.assertIn("нельзя на опасную полку", str(cm.exception))

    def test_receive_batch_calls_super_on_valid_product(self):
        shelf = Shelf("FR-01", BinType.FRIDGE)
        batch = Batch(self.food_product, "B007", 200)
        shelf.receive_batch(batch)
        self.assertEqual(shelf.current_load, 200)
        self.assertIn("P001", shelf.storage)
        self.assertEqual(len(shelf.storage["P001"]), 1)

