
import unittest

from core.product import Product
from storage.location import Location
from storage.warehouse_module import Warehouse
from enums.product_category import Category
from exceptions.errors import WarehouseError


class TestWarehouse(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("Main Warehouse")

        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")


    def test_init_sets_name_and_creates_containers(self):
        self.assertEqual(self.warehouse.name, "Main Warehouse")
        self.assertEqual(self.warehouse.products, {})
        self.assertEqual(self.warehouse.locations, {})
        self.assertIsInstance(self.warehouse.expired_bin, object)  


    def test_register_product_adds_to_products(self):
        self.warehouse.register_product(self.product)
        self.assertIn("P001", self.warehouse.products)
        self.assertEqual(self.warehouse.products["P001"], self.product)

    def test_register_product_raises_if_duplicate_id(self):
        self.warehouse.register_product(self.product)
        with self.assertRaises(WarehouseError) as cm:
            self.warehouse.register_product(self.product)
        self.assertIn("уже зарегистрирован", str(cm.exception))

    def test_add_location_adds_to_locations(self):
        location = Location("A1")
        self.warehouse.add_location(location)
        self.assertIn("A1", self.warehouse.locations)
        self.assertEqual(self.warehouse.locations["A1"], location)

    def test_add_location_raises_if_duplicate_name(self):
        location = Location("A1")
        self.warehouse.add_location(location)
        with self.assertRaises(WarehouseError) as cm:
            self.warehouse.add_location(location)
        self.assertIn("уже существует", str(cm.exception))



    def test_stock_report_returns_dict_with_totals(self):

        self.warehouse.register_product(self.product)


        loc1 = Location("L1")
        loc2 = Location("L2")
        self.warehouse.add_location(loc1)
        self.warehouse.add_location(loc2)

     
        loc1.total_qty = lambda pid: 30 if pid == "P001" else 0
        loc2.total_qty = lambda pid: 20 if pid == "P001" else 0

        report = self.warehouse.stock_report()
        self.assertEqual(report, {"P001": 50})

    def test_stock_report_empty_if_no_products(self):
        report = self.warehouse.stock_report()
        self.assertEqual(report, {})

    def test_stock_report_empty_if_no_locations(self):
        self.warehouse.register_product(self.product)
        report = self.warehouse.stock_report()
        self.assertEqual(report, {"P001": 0})



    def test_total_qty_sums_across_locations(self):
        self.warehouse.register_product(self.product)

        loc1 = Location("L3")
        loc2 = Location("L4")
        self.warehouse.add_location(loc1)
        self.warehouse.add_location(loc2)

        loc1.total_qty = lambda pid: 40 if pid == "P001" else 0
        loc2.total_qty = lambda pid: 10 if pid == "P001" else 0

        total = self.warehouse.total_qty("P001")
        self.assertEqual(total, 50)


    def test_total_qty_returns_zero_if_no_locations(self):
        self.warehouse.register_product(self.product)
        total = self.warehouse.total_qty("P001")
        self.assertEqual(total, 0)

