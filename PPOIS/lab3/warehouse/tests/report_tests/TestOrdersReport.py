
import unittest
from datetime import datetime

from reports.orders_report import OrdersReport
from enums.product_category import Category
from enums.bin_type import BinType
from storage.warehouse_module import Warehouse
from storage.location import Location
from storage.bin import Bin
from storage.batch import Batch
from core.product import Product

class TestOrdersReport(unittest.TestCase):

    def setUp(self):
      
        self.warehouse = Warehouse("Test Warehouse")

        self.p1 = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")
        self.p2 = Product("Bread", "P002", 30, 0.5, Category.FOOD, "PIECE")
        self.warehouse.register_product(self.p1)
        self.warehouse.register_product(self.p2)

        self.loc1 = Location("A1")
        self.loc2 = Location("A2")
        self.warehouse.add_location(self.loc1)
        self.warehouse.add_location(self.loc2)

        self.bin1 = Bin("B1-01", BinType.STANDARD, capacity=1000)
        self.bin2 = Bin("B2-01", BinType.STANDARD, capacity=1000)
        self.loc1.add_bin(self.bin1)
        self.loc2.add_bin(self.bin2)

        self.b1 = Batch(self.p1, "B001", 10)
        self.b2 = Batch(self.p1, "B002", 5)
        self.b3 = Batch(self.p2, "B003", 20)

        self.bin1.receive_batch(self.b1)
        self.bin1.receive_batch(self.b3)
        self.bin2.receive_batch(self.b2)

        self.report = OrdersReport(self.warehouse)


    def test_generate_accumulates_quantities_by_product_name(self):
        data = self.report.generate()

        self.assertIsInstance(self.report.generated_at, datetime)
        self.assertEqual(data, self.report.data)

        self.assertEqual(data["Milk"], 15)  
        self.assertEqual(data["Bread"], 20)

    def test_generate_empty_if_no_batches(self):
        empty_wh = Warehouse("Empty")
        report = OrdersReport(empty_wh)
        data = report.generate()
        self.assertEqual(data, {})

    def test_generate_handles_multiple_locations_and_bins(self):
        loc3 = Location("B1")
        bin3 = Bin("B3-01", BinType.STANDARD, capacity=1000)
        loc3.add_bin(bin3)
        self.warehouse.add_location(loc3)

        b4 = Batch(self.p1, "B004", 7)
        bin3.receive_batch(b4)

        data = self.report.generate()
        self.assertEqual(data["Milk"], 22)  



    def test_accumulate_batches_adds_quantity(self):
        self.report.data = {}
        batches = [Batch(self.p1, "X", 3), Batch(self.p1, "Y", 4)]
        self.report._accumulate_batches(batches)
        self.assertEqual(self.report.data["Milk"], 7)

    def test_accumulate_batches_creates_new_entry(self):
        self.report.data = {}
        batches = [Batch(self.p2, "Z", 5)]
        self.report._accumulate_batches(batches)
        self.assertEqual(self.report.data["Bread"], 5)


    def test_total_quantity_returns_sum_of_all(self):
        self.report.generate()
        total = self.report.total_quantity()
        self.assertEqual(total, 35)  

    def test_total_quantity_calls_generate_if_no_data(self):
        self.assertIsNone(self.report.data)
        total = self.report.total_quantity()
        self.assertEqual(total, 35)
        self.assertIsNotNone(self.report.data)

    def test_total_quantity_zero_if_empty(self):
        empty_wh = Warehouse("Empty")
        report = OrdersReport(empty_wh)
        self.assertEqual(report.total_quantity(), 0)
