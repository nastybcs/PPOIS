from utils.sales_aggregator import SalesAggregator
from orders.order import Order
from core.employee import Employee
from exceptions.errors import OrderError
class OrderManager(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.sales_aggregator = SalesAggregator()
        self.managed_orders = []

    def create_order(self, customer):
        order = Order(customer)
        self.managed_orders.append(order)
        return order

    def assign_driver(self, order, driver):
        if order not in self.managed_orders:
            raise OrderError("Заказ не под вашим управлением")
        return driver.assign_delivery(order, self.sales_aggregator)

    def complete_delivery(self, delivery):
        delivery.complete()
        return "Доставка завершена"

    def get_sales_report(self):
        return self.sales_aggregator.get_report(self.warehouse)