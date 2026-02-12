import unittest
from storage.warehouse_module import Warehouse
from core.product import Product
from enums.product_category import Category
from staff.label_printer import LabelPrinter
from enums.uom import UOM



class TestLabelPrinter(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Тестовый Склад")
        self.product = Product("Молоко", 1, 100, 1.0, Category.FOOD, UOM.LITER)
        self.warehouse.register_product(self.product)
        self.label_printer = LabelPrinter("Иван", "Иванов", "ул. Тестовая, 1", "ivan@mail.com", self.warehouse)

    def test_print_product_label(self):
        result = self.label_printer.print_product_label(self.product, quantity=5)
        self.assertIn("Напечатано 5 этикеток", result)
        self.assertEqual(self.label_printer.printed_labels, 5)

    def test_print_batch_label(self):
        batch = type("Batch", (), {"product": self.product, "batch_id": 101, "quantity": 10})()
        result = self.label_printer.print_batch_label(batch)
        self.assertIn("Этикетка для партии 101", result)
        self.assertEqual(self.label_printer.printed_labels, 1)

    def test_print_product_label_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.label_printer.print_product_label(self.product, 0)

