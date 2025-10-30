import unittest
from staff.loader import Loader
from storage.warehouse_module import Warehouse
from storage.pallet import  Pallet
from storage.batch import Batch
from core.product import Product
from enums.product_category import Category
from exceptions.errors import WarehouseError
from storage.location import Location

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Тестовый Склад")
        self.loader = Loader("Анна", "Петрова", "ул. Логистическая, 1", "anna@mail.com", self.warehouse)
        self.location = Location("A1")
        self.warehouse.add_location(self.location)
        self.loader.assign_location(self.location)

        self.product = Product("Сок", 101, 100, 1, Category.FOOD)
        self.pallet = Pallet("P-001")
        self.location.add_bin(self.pallet)
        self.batch = Batch(self.product, "B-001", 10)

    def test_assign_location_duplicate_raises(self):
        with self.assertRaises(Exception): 
            self.loader.assign_location(self.location)

    def test_load_batch_success(self):
        result = self.loader.load_batch(self.batch, self.location)
        self.assertIn("загрузил партию", result)
        self.assertIn(self.batch.batch_id, self.loader.loaded_batches)
        self.assertEqual(self.pallet.total_qty(self.product.product_id), 10)

    def test_load_batch_location_not_assigned_raises(self):
        other_location = Location("B2")
        with self.assertRaises(WarehouseError):
            self.loader.load_batch(self.batch, other_location)
