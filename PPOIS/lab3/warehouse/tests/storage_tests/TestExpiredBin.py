
import unittest
from datetime import date, timedelta, datetime

from core.product import Product
from storage.batch import Batch
from storage.expired_bin import ExpiredBin
from storage.warehouse_module import Warehouse
from staff.department import HRDepartment

from enums.uom import UOM
from enums.product_category import Category



class TestExpiredBin(unittest.TestCase):

    def setUp(self):

        self.warehouse = Warehouse("Test Warehouse")
        self.hr = HRDepartment(self.warehouse)


        self.checker = self.hr.hire_expiration_checker(
            "Anna", "Ivanova", "Moscow, Lenina, 5", "anna@warehouse.ru"
        )
        self.accountant = self.hr.hire_accountant(
            "Petr", "Sidorov", "Moscow, Petrov St, 10", "petr@warehouse.ru"
        )
        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, UOM.LITER)
        self.expired_bin = ExpiredBin(self.warehouse, "EXPIRED-01")

    def test_init_sets_code_and_warehouse(self):
        self.assertEqual(self.expired_bin.code, "EXPIRED-01")
        self.assertEqual(self.expired_bin.warehouse, self.warehouse)
        self.assertEqual(self.expired_bin.batches, [])
        self.assertEqual(self.expired_bin.total_qty, 0)

    def test_add_expired_batch_success(self):
        exp_date = date.today() - timedelta(days=1)
        batch = Batch(self.product, "B001", 50, exp_date)

        result = self.expired_bin.add_expired_batch(batch, self.checker)
        self.assertIn("перемещена", result)
        self.assertEqual(len(self.expired_bin.batches), 1)
        self.assertEqual(self.expired_bin.total_qty, 50)

        entry = self.expired_bin.batches[0]
        self.assertEqual(entry["batch"], batch)
        self.assertEqual(entry["moved_by"], "Anna Ivanova")
        self.assertIsInstance(entry["moved_at"], datetime)

    def test_add_expired_batch_raises_if_not_expired(self):
        exp_date = date.today() + timedelta(days=1)
        batch = Batch(self.product, "B002", 30, exp_date)

        with self.assertRaises(ValueError) as cm:
            self.expired_bin.add_expired_batch(batch, self.checker)
        self.assertIn("не просрочена", str(cm.exception))

    def test_add_expired_batch_raises_if_no_exp_date(self):
        batch = Batch(self.product, "B003", 20)

        with self.assertRaises(ValueError):
            self.expired_bin.add_expired_batch(batch, self.checker)


    def test_clear_empties_bin_and_resets_qty(self):
        batch = Batch(self.product, "B004", 10, date.today() - timedelta(days=1))
        self.expired_bin.add_expired_batch(batch, self.checker)

        result = self.expired_bin.clear(self.accountant)
        self.assertIn("очищена", result)
        self.assertIn("Petr Sidorov", result)
        self.assertEqual(len(self.expired_bin.batches), 0)
        self.assertEqual(self.expired_bin.total_qty, 0)

    def test_clear_returns_empty_message_if_no_batches(self):
        result = self.expired_bin.clear(self.accountant)
        self.assertEqual(result, "Корзина пуста")

    def test_report_returns_correct_structure(self):
        batch = Batch(self.product, "B005", 15, date.today() - timedelta(days=2))
        self.expired_bin.add_expired_batch(batch, self.checker)

        report = self.expired_bin.report()

        self.assertEqual(report["code"], "EXPIRED-01")
        self.assertEqual(report["total_batches"], 1)
        self.assertEqual(report["total_qty"], 15)

        item = report["contents"][0]
        self.assertEqual(item["product"], "Milk")
        self.assertEqual(item["batch_id"], "B005")
        self.assertEqual(item["qty"], 15)
        self.assertEqual(item["exp_date"], batch.exp_date)
        self.assertEqual(item["moved_by"], "Anna Ivanova")

    def test_report_empty_bin(self):
        report = self.expired_bin.report()
        self.assertEqual(report["total_batches"], 0)
        self.assertEqual(report["total_qty"], 0)
        self.assertEqual(report["contents"], [])
