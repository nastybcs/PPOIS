import unittest
import datetime

from core.product import Product
from orders.delivery import Delivery
from staff.department import HRDepartment
from storage.warehouse_module import Warehouse
from exceptions.errors import DeliveryError
from enums.order_status import OrderStatus
from enums.delivery_status import DeliveryStatus
from enums.uom import UOM
from enums.product_category import Category


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("Главный склад")
        self.hr = HRDepartment(self.warehouse)

      
        self.order_manager = self.hr.hire_order_manager(
            "Анна", "Смирнова", "Москва, Тверская, 1", "anna@warehouse.ru"
        )
        self.aggregator = self.order_manager.sales_aggregator

     
        self.customer = self.hr.register_customer(
            "Иван", "Иванов", "Москва, Ленина, 10"
        )

       
        self.driver1 = self.hr.hire_driver(
            "Алексей", "Петров", "Москва, Лесная, 5", "a@petrov.ru", "A123BC"
        )
        self.driver2 = self.hr.hire_driver(
            "Михаил", "Сидоров", "СПб, Невский, 1", "m@sidorov.ru", "B456XY"
        )

 
        self.product1 = Product("Молоко", "P001", 70, 1.0, Category.FOOD, UOM.LITER)
        self.product2 = Product("Хлеб", "P002", 40, 0.5, Category.FOOD, UOM.PIECE)


        self.order1 = self.order_manager.create_order(self.customer)
        self.order2 = self.order_manager.create_order(self.customer)
        self.order3 = self.order_manager.create_order(self.customer)


    def test_order_initialization(self):
        order = self.order_manager.create_order(self.customer)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.items, [])
        self.assertEqual(order.status, OrderStatus.CREATED)
        self.assertGreater(order.order_id, 0)

    def test_order_id_counter(self):
        self.assertEqual(self.order2.order_id, self.order1.order_id + 1)

    def test_add_item(self):
        self.order1.add_item(self.product1, 2)
        self.assertEqual(len(self.order1.items), 1)
        self.assertEqual(self.order1.items[0].product, self.product1)
        self.assertEqual(self.order1.items[0].quantity, 2)

    def test_total_amount(self):
        self.order1.add_item(self.product1, 2)
        self.order1.add_item(self.product2, 3)
        self.assertEqual(self.order1.total_amount(), 140 + 120)

    def test_total_amount_empty(self):
        self.assertEqual(self.order1.total_amount(), 0)

    def test_order_item_total_price(self):
        self.order1.add_item(self.product1, 5)
        self.assertEqual(self.order1.items[0].total_price(), 350)


    def test_assign_delivery_success(self):
        delivery = self.order_manager.assign_driver(self.order1, self.driver1)

        self.assertIsInstance(delivery, Delivery)
        self.assertEqual(delivery.driver, self.driver1)
        self.assertEqual(delivery.order, self.order1)
        self.assertEqual(delivery.status, DeliveryStatus.ASSIGNED)
        self.assertIs(self.order1.delivery, delivery)

    def test_assign_delivery_twice_raises_error(self):
        self.order_manager.assign_driver(self.order1, self.driver1)
        with self.assertRaises(DeliveryError):
            self.order_manager.assign_driver(self.order1, self.driver1)

    def test_delivery_driver_has_delivery_in_list(self):
        self.assertEqual(len(self.driver1.deliveries), 0)
        self.order_manager.assign_driver(self.order1, self.driver1)
        self.assertEqual(len(self.driver1.deliveries), 1)
        self.assertIs(self.driver1.deliveries[0], self.order1.delivery)

    def test_assign_delivery_different_drivers(self):
        d1 = self.order_manager.assign_driver(self.order1, self.driver1)
        d2 = self.order_manager.assign_driver(self.order2, self.driver2)
        self.assertEqual(d1.driver, self.driver1)
        self.assertEqual(d2.driver, self.driver2)

    def test_delivery_status_after_assignment(self):
        delivery = self.order_manager.assign_driver(self.order1, self.driver1)
        self.assertEqual(delivery.status, DeliveryStatus.ASSIGNED)


    def test_assign_delivery_with_same_driver_multiple_orders(self):
        d1 = self.order_manager.assign_driver(self.order1, self.driver1)
        d2 = self.order_manager.assign_driver(self.order2, self.driver1)
        d3 = self.order_manager.assign_driver(self.order3, self.driver1)

        self.assertEqual(len(self.driver1.deliveries), 3)
        self.assertIn(d1, self.driver1.deliveries)
        self.assertIn(d2, self.driver1.deliveries)
        self.assertIn(d3, self.driver1.deliveries)

    def test_delivery_has_correct_id_and_timestamp(self):
        d1 = self.order_manager.assign_driver(self.order1, self.driver1)
        before = datetime.datetime.now()
        d2 = self.order_manager.assign_driver(self.order2, self.driver1)

        self.assertEqual(d2.delivery_id, d1.delivery_id + 1)
        self.assertLess(d1.assigned_at, before)


if __name__ == '__main__':
    unittest.main(verbosity=2)