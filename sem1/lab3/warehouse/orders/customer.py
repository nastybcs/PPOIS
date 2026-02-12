from core.person import Person
from orders.order import Order
from enums.order_status import OrderStatus
from core.address import Address
class Customer(Person):
    def __init__(self, first_name, last_name, address, email=None):
        if isinstance(address, str):
            city, street, house = address.split(", ", 2)
            address = Address(city, street, house)
        super().__init__(first_name, last_name, address, email)
        self.orders = []

    def create_order(self):
        order = Order(self)
        self.orders.append(order)
        return order

    def total_spent(self):
        return sum(order.total_amount() for order in self.orders if order.status == OrderStatus.DELIVERED)