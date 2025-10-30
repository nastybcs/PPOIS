
import unittest
import datetime
from core.product import Product
from storage.warehouse_module import Warehouse
from orders.delivery import Delivery
from staff.department import HRDepartment
from enums.delivery_status import DeliveryStatus
from enums.order_status import OrderStatus
from enums.uom import UOM
from enums.product_category import Category
from exceptions.errors import DeliveryError


class TestDelivery(unittest.TestCase):

    def setUp(self):
      
        self.warehouse = Warehouse("Test Warehouse")
        self.hr = HRDepartment(self.warehouse)

    
        self.order_manager = self.hr.hire_order_manager(
            "OM", "Test", "Moscow, Test St, 1", "om@test.ru"
        )
        self.aggregator = self.order_manager.sales_aggregator

        self.customer = self.hr.register_customer(
            "Ivan", "Ivanov", "Moscow, Lenina, 10"
        )

      
        self.driver = self.hr.hire_driver(
            "Alex", "Petrov", "Moscow, Petrov St, 5", "alex@petrov.ru", "A123BC"
        )

      
        self.product = Product(
            name="Молоко",
            product_id="P001",
            price=70,
            weight=1.0,
            category=Category.FOOD,
            uom=UOM.LITER
        )
        self.warehouse.register_product(self.product) 

        self.order = self.order_manager.create_order(self.customer)
        self.order.add_item(self.product, 2)


    def test_delivery_init_sets_id_and_timestamp(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)

        self.assertEqual(delivery.delivery_id, 8)
        self.assertEqual(delivery.driver, self.driver)
        self.assertEqual(delivery.order, self.order)
        self.assertEqual(delivery.destination, self.customer.address)
        self.assertEqual(delivery.status, DeliveryStatus.PENDING)
        self.assertIsNotNone(delivery.assigned_at)
        self.assertLess(delivery.assigned_at, datetime.datetime.now())

    def test_delivery_id_counter_increments(self):
        d1 = Delivery(self.driver, self.order, self.aggregator)
        order2 = self.order_manager.create_order(self.customer)
        d2 = Delivery(self.driver, order2, self.aggregator)
        self.assertEqual(d2.delivery_id, d1.delivery_id + 1)

    def test_start_changes_status_to_in_transit(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        delivery.start()
        self.assertEqual(delivery.status, DeliveryStatus.IN_TRANSIT)

    def test_start_raises_if_not_pending(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)

        delivery.status = DeliveryStatus.IN_TRANSIT
        with self.assertRaises(DeliveryError):
            delivery.start()

        delivery.status = DeliveryStatus.CANCELLED
        with self.assertRaises(DeliveryError):
            delivery.start()

 


    def test_complete_sets_delivered_and_updates_order(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        delivery.start()
        delivery.complete()

        self.assertEqual(delivery.status, DeliveryStatus.DELIVERED)
        self.assertEqual(self.order.status, OrderStatus.DELIVERED)
        self.assertIsNotNone(delivery.completed_at)

    
        report = self.aggregator.get_report(self.warehouse)
        self.assertIn("Молоко", report)
        self.assertEqual(report["Молоко"]["sold_qty"], 2)
        self.assertEqual(report["Молоко"]["total_amount"], 140)

    def test_complete_raises_if_not_in_transit(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)

        with self.assertRaises(DeliveryError):
            delivery.complete() 

        delivery.start()
        delivery.complete()  
        with self.assertRaises(DeliveryError):
            delivery.complete()  



    def test_cancel_sets_cancelled(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        delivery.cancel()
        self.assertEqual(delivery.status, DeliveryStatus.CANCELLED)

    def test_cancel_raises_if_already_delivered(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        delivery.start()
        delivery.complete()
        with self.assertRaises(DeliveryError):
            delivery.cancel()

    def test_cancel_allowed_if_in_transit(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        delivery.start()
        delivery.cancel()
        self.assertEqual(delivery.status, DeliveryStatus.CANCELLED)



    def test_info_returns_correct_dict(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        info = delivery.info()

        self.assertEqual(info["delivery_id"], 10)
        self.assertEqual(info["driver"], "Alex Petrov")
        self.assertEqual(info["order_id"], self.order.order_id)
        self.assertIn("Moscow", info["destination"])
        self.assertIn("Moscow", info["destination"])
        self.assertIn("Lenina", info["destination"])
        self.assertIn("10", info["destination"])
        self.assertEqual(info["status"], "в ожидании")
        

    def test_info_after_complete(self):
        delivery = Delivery(self.driver, self.order, self.aggregator)
        delivery.start()
        delivery.complete()
        info = delivery.info()
        self.assertEqual(info["status"], "доставлено")
