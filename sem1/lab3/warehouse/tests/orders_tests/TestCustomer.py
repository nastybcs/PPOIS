import unittest
from core.address import Address
from orders.customer import Customer
from orders.order import Order
from enums.order_status import OrderStatus
from core.product import Product
from enums.product_category import Category
from enums.uom import UOM
class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.address = Address(city="Moscow", street="Lenina", house_num="10A")
        self.customer = Customer("Ivan", "Ivanov", self.address, "ivan@example.com")
        self.product1 = Product("Apple", 1, 100, 0.2, Category.FOOD, UOM.KILOGRAM)
        self.product2 = Product("Laptop", 2, 50000, 2, Category.ELECTRONICS, UOM.PIECE)

    def test_create_customer(self):
        self.assertEqual(self.customer.first_name, "Ivan")
        self.assertEqual(self.customer.last_name, "Ivanov")
        self.assertEqual(self.customer.address, self.address)
        self.assertEqual(self.customer.email, "ivan@example.com")
        self.assertEqual(len(self.customer.orders), 0)

    def test_create_order(self):
        order = self.customer.create_order()
        self.assertEqual(len(self.customer.orders), 1)
        self.assertIn(order, self.customer.orders)
        self.assertEqual(order.customer, self.customer)

    def test_total_spent_only_delivered(self):
        order1 = self.customer.create_order()
        order1.add_item(self.product1, 2)
        order1.add_item(self.product2, 1)
        order1.status = OrderStatus.DELIVERED

        order2 = self.customer.create_order()
        order2.add_item(self.product1, 1)
        order2.status = OrderStatus.CREATED

        expected_total = sum(item.total_price() for order in self.customer.orders
                             for item in order.items if order.status == OrderStatus.DELIVERED)
        total = self.customer.total_spent()
        self.assertEqual(total, expected_total)
  