import unittest
from storage.warehouse_module import Warehouse
from core.product import Product
from enums.product_category import Category
from staff.receipt_printer import ReceiptPrinter
from orders.customer import Customer
from orders.order import Order
from enums.order_status import OrderStatus
from enums.uom import UOM

class TestReceiptPrinter(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Тестовый Склад")
        self.product1 = Product("Молоко", 1, 100, 1.0, Category.FOOD, UOM.LITER)
        self.product2 = Product("Хлеб", 2, 50, 0.5, Category.FOOD, UOM.PIECE)
        self.warehouse.register_product(self.product1)
        self.warehouse.register_product(self.product2)
        self.receipt_printer = ReceiptPrinter("Пётр", "Петров", "ул. Примерная, 2", "petr@mail.com", self.warehouse)
        self.customer = Customer("Анна", "Смирнова", "Москва, Ленина, 10")

    def test_print_receipt_for_delivered_order(self):
        order = Order(self.customer)
        order.add_item(self.product1, 2)
        order.add_item(self.product2, 3)
        order.status = OrderStatus.DELIVERED

        receipt = self.receipt_printer.print_receipt(order)
        self.assertIn("ЧЕК #1", receipt)
        self.assertIn("Молоко x2", receipt)
        self.assertIn("Хлеб x3", receipt)
        self.assertEqual(self.receipt_printer.printed_receipts, 1)

    def test_print_receipt_for_undelivered_order_raises(self):
        order = Order(self.customer)
        order.add_item(self.product1, 1)
        order.status = OrderStatus.CREATED

        with self.assertRaises(ValueError):
            self.receipt_printer.print_receipt(order)