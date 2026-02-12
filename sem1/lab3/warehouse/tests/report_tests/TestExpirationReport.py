
import unittest
from datetime import date, timedelta

from reports.expration_report import ExpirationReport
from core.employee import Employee
from enums.product_category import Category
from enums.bin_type import BinType
from storage.warehouse_module import Warehouse
from storage.location import Location
from storage.batch import Batch
from core.product import Product
from core.address import Address
from storage.bin import Bin
from staff.department import HRDepartment

class TestExpirationReport(unittest.TestCase):

    def setUp(self):
     
        self.warehouse = Warehouse("Test Warehouse")

        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")
        self.warehouse.register_product(self.product)

        self.loc1 = Location("A1")
        self.loc2 = Location("A2")
        self.warehouse.add_location(self.loc1)
        self.warehouse.add_location(self.loc2)

        self.bin1 = Bin("B1-01", BinType.STANDARD, capacity=1000)
        self.bin2 = Bin("B2-01", BinType.STANDARD, capacity=1000)
        self.loc1.add_bin(self.bin1)
        self.loc2.add_bin(self.bin2)

        self.batch_expired1 = Batch(
            self.product, "B001", 10,
            exp_date=date.today() - timedelta(days=1)
        )
        self.batch_expired2 = Batch(
            self.product, "B002", 5,
            exp_date=date.today() - timedelta(days=5)
        )
        self.batch_fresh = Batch(
            self.product, "B003", 20,
            exp_date=date.today() + timedelta(days=10)
        )

        self.bin1.receive_batch(self.batch_expired1)
        self.bin1.receive_batch(self.batch_fresh)
        self.bin2.receive_batch(self.batch_expired2)

        self.hr = HRDepartment(self.warehouse)
        self.checker = self.hr.hire_expiration_checker("Anna", "Sidorova", "Moscow", "anna@wh")

        self.report = ExpirationReport(self.warehouse)

 

    def test_init_calls_super(self):
        self.assertEqual(self.report.warehouse, self.warehouse)
        self.assertIsNone(self.report.data)


    def test_generate_collects_expired_batches(self):
        data = self.report.generate(self.checker)

        self.assertEqual(data["checker"], "Anna Sidorova")
        self.assertEqual(data["expired_batches"], 2)
        self.assertIn("T", data["generated_at"])

        details = data["details"]
        self.assertEqual(len(details), 2)

        batch_ids = [d["batch_id"] for d in details]
        self.assertIn("B001", batch_ids)
        self.assertIn("B002", batch_ids)

        for d in details:
            self.assertIn("product", d)
            self.assertIn("exp_date", d)
            self.assertIn("qty", d)

    def test_generate_empty_if_no_expired(self):

        self.bin1.storage.clear()
        self.bin2.storage.clear()

        data = self.report.generate(self.checker)
        self.assertEqual(data["expired_batches"], 0)
        self.assertEqual(data["details"], [])

    def test_generate_empty_if_no_locations(self):
        empty_wh = Warehouse("Empty")
        report = ExpirationReport(empty_wh)
        checker = Employee("Test", "User", "SPb", "test", empty_wh)

        data = report.generate(checker)
        self.assertEqual(data["expired_batches"], 0)
        self.assertEqual(data["details"], [])

    def test_generate_uses_real_expiration_checker(self):

        self.assertEqual(len(self.checker.checked_batches), 0)
        self.report.generate(self.checker)
        self.assertGreater(len(self.checker.checked_batches), 0)

