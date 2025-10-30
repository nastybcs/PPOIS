
import unittest
from datetime import datetime

from reports.delivery_report import DeliveryReport
from enums.delivery_status import DeliveryStatus
from enums.order_status import OrderStatus
from storage.warehouse_module import Warehouse
from staff.department import HRDepartment
from orders.order import Order
from orders.delivery import Delivery
from orders.customer import Customer
from core.address import Address


class TestDeliveryReport(unittest.TestCase):

    def setUp(self):

        self.warehouse = Warehouse("Test Warehouse")
        self.hr = HRDepartment(self.warehouse)

        self.driver = self.hr.hire_driver(
            "Ivan", "Petrov", "Moscow", "ivan@petrov", "A123BC"
        )

        self.address = Address("Moscow", "Lenina", "10")
        self.customer = Customer("Anna", "Ivanova", self.address, "anna@email.com")

        self.order1 = self.customer.create_order()
        self.order1.order_id = 101
        self.order1.status = OrderStatus.CREATED

        self.order2 = self.customer.create_order()
        self.order2.order_id = 102
        self.order2.status = OrderStatus.CREATED

        self.aggregator = type("Agg", (), {"record_delivery": lambda x: None})()

        self.delivery1 = Delivery(self.driver, self.order1, self.aggregator)
        self.delivery1.status = DeliveryStatus.DELIVERED

        self.delivery2 = Delivery(self.driver, self.order2, self.aggregator)
        self.delivery2.status = DeliveryStatus.IN_TRANSIT  

        self.driver.deliveries.extend([self.delivery1, self.delivery2])

        self.report = DeliveryReport(self.warehouse, self.hr)

    def test_init_calls_super_and_sets_hr(self):
        self.assertEqual(self.report.warehouse, self.warehouse)
        self.assertEqual(self.report.hr, self.hr)
        self.assertIsNone(self.report.generated_at)
        self.assertIsNone(self.report.data)

    def test_generate_creates_correct_report_structure(self):
        data = self.report.generate()

        self.assertIsInstance(self.report.generated_at, datetime)
        self.assertEqual(data, self.report.data)

        ivan_report = data["Ivan Petrov"]
        self.assertEqual(len(ivan_report), 2)

        d1 = ivan_report[0]
        self.assertEqual(d1["order_id"], 101)
        self.assertEqual(d1["status"], DeliveryStatus.DELIVERED.value)  
        self.assertEqual(d1["destination"], "Moscow, Lenina, 10")

        d2 = ivan_report[1]
        self.assertEqual(d2["order_id"], 102)
        self.assertEqual(d2["status"], DeliveryStatus.IN_TRANSIT.value)  

    def test_generate_empty_if_no_drivers(self):
        empty_hr = type("HR", (), {"drivers": []})()
        r = DeliveryReport(self.warehouse, empty_hr)
        self.assertEqual(r.generate(), {})

    def test_generate_empty_if_driver_has_no_deliveries(self):
        new_driver = self.hr.hire_driver("Max", "Sidorov", "SPb", "max", "X999")
        data = self.report.generate()
        self.assertIn("Max Sidorov", data)
        self.assertEqual(data["Max Sidorov"], [])

    def test_total_deliveries_counts_all(self):
        self.report.generate()
        total = self.report.total_deliveries()
        self.assertEqual(total, 2)

    def test_total_deliveries_calls_generate_if_no_data(self):
        self.assertIsNone(self.report.data)
        total = self.report.total_deliveries()
        self.assertEqual(total, 2)
        self.assertIsNotNone(self.report.data)

    def test_total_deliveries_returns_zero_if_no_data_after_generate(self):
        empty_hr = type("HR", (), {"drivers": []})()
        r = DeliveryReport(self.warehouse, empty_hr)
        total = r.total_deliveries()
        self.assertEqual(total, 0)

