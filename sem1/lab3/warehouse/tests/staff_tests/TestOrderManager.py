import unittest
from staff.order_manager import OrderManager
from orders.customer import Customer
from storage.warehouse_module import Warehouse
from staff.driver import Driver
from orders.delivery import Delivery
from orders.order import Order
from core.address import Address

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Тестовый Склад")
        self.manager = OrderManager("Мария", "Иванова", "ул. Логистическая, 2", "maria@mail.com", self.warehouse)
        self.customer = Customer("Петр", "Петров", Address("Москва", "Ленина", "10"))
        self.driver = Driver("Иван", "Иванов", "ул. Водительская, 5", "ivan@mail.com", self.warehouse, "A123BC")

    def test_create_order(self):
        order = self.manager.create_order(self.customer)
        self.assertIsInstance(order, Order)
        self.assertIn(order, self.manager.managed_orders)
        self.assertEqual(order.customer, self.customer)

    def test_assign_driver_success(self):
        order = self.manager.create_order(self.customer)
        delivery = self.manager.assign_driver(order, self.driver)
        self.assertIsInstance(delivery, Delivery)
        self.assertIn(delivery, self.driver.deliveries)
        self.assertEqual(delivery.order, order)
        self.assertEqual(delivery.driver, self.driver)

    def test_assign_driver_order_not_managed_raises(self):
        order = Order(self.customer)
        with self.assertRaises(Exception): 
            self.manager.assign_driver(order, self.driver)



