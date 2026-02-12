
import unittest

from transport.vehicle import Vehicle
from enums.vehicle_type import VehicleType
from staff.driver import Driver
from orders.order import Order
from orders.order_item import OrderItem
from core.product import Product
from enums.product_category import Category


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.warehouse = type("Warehouse", (), {"name": "Test Warehouse"})
        self.driver = Driver("Ivan", "Petrov", "Moscow", "ivan@petrov", self.warehouse, "A123BC")
        self.vehicle = Vehicle("A123BC", "Ford Transit", VehicleType.VAN, 1500)


    def test_init_sets_attributes_and_default_capacity(self):
        self.assertEqual(self.vehicle.number, "A123BC")
        self.assertEqual(self.vehicle.model, "Ford Transit")
        self.assertEqual(self.vehicle.type, VehicleType.VAN)
        self.assertEqual(self.vehicle.capacity_kg, 1500)  
        self.assertEqual(self.vehicle.current_load, 0)
        self.assertTrue(self.vehicle.is_available)

    def test_init_uses_custom_capacity(self):
        v = Vehicle("X999", "Big Truck", VehicleType.TRUCK, capacity_kg=20000)
        self.assertEqual(v.capacity_kg, 20000)


    def test_assign_driver_success(self):
        result = self.vehicle.assign_driver(self.driver)
        self.assertEqual(self.vehicle.driver, self.driver)
        self.assertEqual(self.driver.vehicle, self.vehicle)
        self.assertIn("закреплён", result)

    def test_assign_driver_raises_if_already_assigned(self):
        self.vehicle.assign_driver(self.driver)
        other_driver = Driver("Petr", "Ivanov", "SPb", "petr", self.warehouse, "B456XY")
        with self.assertRaises(ValueError) as cm:
            self.vehicle.assign_driver(other_driver)
        self.assertIn("уже закреплена", str(cm.exception))


    def test_load_order_success(self):
        product = Product("Milk", "P001", 70, 10.0, Category.FOOD, "KG")  
        item = OrderItem(product, quantity=50)  
        order = Order(None)
        order.items.append(item)

        self.vehicle.load_order(order)
        self.assertEqual(self.vehicle.current_load, 500)

    def test_load_order_raises_if_over_capacity(self):
        product = Product("Bricks", "P002", 100, 20.0, Category.CHEMICAL, "KG")  
        item = OrderItem(product, quantity=100) 
        order = Order(None)
        order.items.append(item)

        with self.assertRaises(ValueError) as cm:
            self.vehicle.load_order(order)
        self.assertIn("Превышена грузоподъёмность", str(cm.exception))

    def test_load_order_handles_missing_weight(self):
        product = Product("Book", "P003", 15, None, Category.FOOD, "PCS")
        item = OrderItem(product, quantity=100)
        order = Order(None)
        order.items.append(item)

        self.vehicle.load_order(order)
        self.assertEqual(self.vehicle.current_load, 0)

    def test_load_order_handles_zero_weight(self):
        product = Product("Air", "P004", 0, 0, Category.FOOD, "M3")
        item = OrderItem(product, quantity=1000)
        order = Order(None)
        order.items.append(item)

        self.vehicle.load_order(order)
        self.assertEqual(self.vehicle.current_load, 0)

    def test_load_order_accumulates_load(self):
        product = Product("Box", "P005", 50, 5.0, Category.FOOD, "KG")
        item1 = OrderItem(product, 20)  
        item2 = OrderItem(product, 30)  
        order1 = Order(None)
        order1.items.append(item1)
        order2 = Order(None)
        order2.items.append(item2)

        self.vehicle.load_order(order1)
        self.vehicle.load_order(order2)
        self.assertEqual(self.vehicle.current_load, 250)


    def test_unload_resets_current_load(self):
        product = Product("Water", "P006", 10, 1.0, Category.FOOD, "LITER")
        item = OrderItem(product, 100)  
        order = Order(None)
        order.items.append(item)
        self.vehicle.load_order(order)
        self.vehicle.unload()
        self.assertEqual(self.vehicle.current_load, 0)


    def test_str_returns_formatted_string(self):
        expected = "фургон Ford Transit (A123BC), вместимость: 1500 кг"
        self.assertEqual(str(self.vehicle), expected)

    def test_str_with_custom_capacity(self):
        v = Vehicle("T001", "KamAZ", VehicleType.TRUCK, capacity_kg=12000)
        expected = "грузовик KamAZ (T001), вместимость: 12000 кг"
        self.assertEqual(str(v), expected)
