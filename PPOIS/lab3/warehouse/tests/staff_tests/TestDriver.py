
import unittest

from core.product import Product
from storage.warehouse_module import Warehouse
from orders.customer import Customer
from orders.order import Order
from orders.delivery import Delivery
from utils.sales_aggregator import SalesAggregator
from staff.department import HRDepartment
from staff.driver import Driver
from transport.route import Route
from transport.route_point import RoutePoint
from exceptions.errors import DeliveryError
from enums.delivery_status import DeliveryStatus
from enums.order_status import OrderStatus
from enums.uom import UOM
from enums.product_category import Category
from enums.route_status import RouteStatus


class TestDriver(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("Test Warehouse")
        self.hr = HRDepartment(self.warehouse)

        self.order_manager = self.hr.hire_order_manager("OM", "Test", "Addr", "om@test")
        self.aggregator = self.order_manager.sales_aggregator

        self.customer = self.hr.register_customer("Ivan", "Ivanov", "Moscow, Lenina, 10")

        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, UOM.LITER)
        self.warehouse.register_product(self.product)

        self.driver = self.hr.hire_driver("Alex", "Petrov", "Moscow", "a@petrov", "A123BC")

        self.order = self.order_manager.create_order(self.customer)
        self.order.add_item(self.product, 1)


    def test_assign_route_success(self):
        point = RoutePoint(self.customer.address)
        route = Route(self.driver, None)
        route.add_point(point)
        result = self.driver.assign_route(route)
        self.assertIn(route, self.driver.routes)
        self.assertIn("назначен", result)

    def test_assign_route_raises_if_wrong_driver(self):
        other_driver = self.hr.hire_driver("Bob", "Smith", "SPb", "bob", "B456XY")
        route = Route(other_driver, None)
        with self.assertRaises(DeliveryError):
            self.driver.assign_route(route)


    def test_start_and_complete_route(self):
        point = RoutePoint(self.customer.address)
        route = Route(self.driver, None)
        route.add_point(point)
        self.driver.assign_route(route)

        self.driver.start_route(route)
        self.assertEqual(route.status, RouteStatus.IN_PROGRESS)

        route.mark_point_visited(0)
        self.driver.complete_route(route)
        self.assertEqual(route.status, RouteStatus.COMPLETED)
        self.assertIsNotNone(route.completed_at)



    def test_assign_delivery_success(self):
        delivery = self.driver.assign_delivery(self.order, self.aggregator)
        self.assertEqual(delivery.status, DeliveryStatus.ASSIGNED)
        self.assertEqual(self.order.delivery, delivery)
        self.assertIn(delivery, self.driver.deliveries)

    def test_assign_delivery_raises_if_already_has_delivery(self):
        self.driver.assign_delivery(self.order, self.aggregator)
        with self.assertRaises(DeliveryError):
            self.driver.assign_delivery(self.order, self.aggregator)



    def test_start_delivery_success(self):
        delivery = self.driver.assign_delivery(self.order, self.aggregator)
        self.driver.start_delivery(delivery)
        self.assertEqual(delivery.status, DeliveryStatus.IN_TRANSIT)

    def test_start_delivery_raises_if_not_assigned(self):
        other_driver = self.hr.hire_driver("Max", "Ivanov", "Kazan", "max", "C789DE")
        delivery = other_driver.assign_delivery(self.order, self.aggregator)
        with self.assertRaises(DeliveryError):
            self.driver.start_delivery(delivery)


    def test_complete_delivery_success(self):
        delivery = self.driver.assign_delivery(self.order, self.aggregator)
        self.driver.start_delivery(delivery)
        self.driver.complete_delivery(delivery)

        self.assertEqual(delivery.status, DeliveryStatus.DELIVERED)
        self.assertEqual(self.order.status, OrderStatus.DELIVERED)
        self.assertIsNotNone(delivery.completed_at)

        report = self.aggregator.get_report(self.warehouse)
        self.assertEqual(report["Milk"]["sold_qty"], 1)
        self.assertEqual(report["Milk"]["total_amount"], 70)

    def test_complete_delivery_raises_if_not_assigned(self):
        other_driver = self.hr.hire_driver("Max", "Ivanov", "Kazan", "max", "C789DE")
        delivery = other_driver.assign_delivery(self.order, self.aggregator)
        delivery.status = DeliveryStatus.IN_TRANSIT
        with self.assertRaises(DeliveryError):
            self.driver.complete_delivery(delivery)


    def test_cancel_delivery_success(self):
        delivery = self.driver.assign_delivery(self.order, self.aggregator)
        self.driver.cancel_delivery(delivery)
        self.assertEqual(delivery.status, DeliveryStatus.CANCELLED)

    def test_cancel_delivery_raises_if_not_assigned(self):
        other_driver = self.hr.hire_driver("Max", "Ivanov", "Kazan", "max", "C789DE")
        delivery = other_driver.assign_delivery(self.order, self.aggregator)
        with self.assertRaises(DeliveryError):
            self.driver.cancel_delivery(delivery)

    def test_cancel_delivery_raises_if_already_delivered(self):
        delivery = self.driver.assign_delivery(self.order, self.aggregator)
        self.driver.start_delivery(delivery)
        self.driver.complete_delivery(delivery)
        with self.assertRaises(DeliveryError):
            self.driver.cancel_delivery(delivery)
