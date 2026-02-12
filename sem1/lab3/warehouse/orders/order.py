from datetime import datetime
from orders.order_item import OrderItem
from exceptions.errors import *
from enums.order_status import OrderStatus
class Order:
    _id_counter = 1

    def __init__(self, customer):
        self.order_id = Order._id_counter
        Order._id_counter += 1
        self.customer = customer
        self.items = []
        self.status = OrderStatus.CREATED
        self.created_at = datetime.now()
        self.delivery = None

    def _items(self):
        return self.items

    def add_item(self, product, quantity):
        self.items.append(OrderItem(product, quantity))

    def total_amount(self):
        return sum(item.total_price() for item in self.items)
    
    def delivery(self, value):
        if self._delivery is not None:
            raise DeliveryError("Доставка уже назначена")
        self._delivery = value
    


