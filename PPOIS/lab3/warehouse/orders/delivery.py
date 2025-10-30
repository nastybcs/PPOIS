import datetime
from enums.delivery_status import DeliveryStatus
from exceptions.errors import DeliveryError
from enums.order_status import OrderStatus


class Delivery:
    _id_counter = 1

    def __init__(self, driver, order,aggregator=None):
        if hasattr(order, "delivery") and order.delivery is not None:
            raise DeliveryError(f"Заказ {order.order_id} уже имеет доставку")

        self.delivery_id = Delivery._id_counter
        Delivery._id_counter += 1

        self.driver = driver
        self.order = order
        self.destination = order.customer.address
        self.status = DeliveryStatus.PENDING  
        self.assigned_at = datetime.datetime.now()
        self.completed_at = None
        self.aggregator = aggregator

    def start(self):
        if self.status not in (DeliveryStatus.PENDING, DeliveryStatus.ASSIGNED):
            raise DeliveryError("Доставка уже начата или отменена")
        self.status = DeliveryStatus.IN_TRANSIT

    def complete(self):
        if self.status != DeliveryStatus.IN_TRANSIT:
            raise DeliveryError("Нельзя завершить доставку, если она не в пути")
        self.status = DeliveryStatus.DELIVERED
        self.completed_at = datetime.datetime.now()
        self.order.status = OrderStatus.DELIVERED
        self.aggregator.record_delivery(self.order)

    def cancel(self):
        if self.status == DeliveryStatus.DELIVERED:
            raise DeliveryError("Нельзя отменить уже доставленный заказ")
        self.status = DeliveryStatus.CANCELLED
        

    def info(self):
        return {
            "delivery_id": self.delivery_id,
            "driver": self.driver.full_name(),
            "order_id": self.order.order_id,
            "destination": self.destination.full_address(),  # ← .full_address()
            "status": self.status.value,
        }

