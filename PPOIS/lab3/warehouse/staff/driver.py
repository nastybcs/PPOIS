from core.employee import Employee
from orders.delivery import Delivery
from exceptions.errors import *
from enums.delivery_status import DeliveryStatus
class Driver(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse, vehicle_number):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.vehicle_number = vehicle_number
        self.deliveries = []  
        self.routes = []

    def assign_route(self, route):
        if route.driver != self:
            raise DeliveryError("Этот маршрут принадлежит другому водителю")
        self.routes.append(route)
        return f"Маршрут {route.route_id} назначен водителю {self.full_name()}"
    def start_route(self, route):
        route.start()

    def complete_route(self, route):
        route.complete()

    def assign_delivery(self, order, aggregator):
        if hasattr(order, "delivery") and order.delivery is not None:
            raise DeliveryError("Уже есть доставка")
        delivery = Delivery(self, order, aggregator)
        order.delivery = delivery
        delivery.status = DeliveryStatus.ASSIGNED
        self.deliveries.append(delivery)
        return delivery
    def start_delivery(self, delivery):
       
        if delivery not in self.deliveries:
            raise DeliveryError(f"Доставка {delivery.delivery_id} не назначена этому водителю")
        delivery.start()

    def complete_delivery(self, delivery):

        if delivery not in self.deliveries:
            raise DeliveryError(f"Доставка {delivery.delivery_id} не назначена этому водителю")
        delivery.complete()

    def cancel_delivery(self, delivery):

        if delivery not in self.deliveries:
            raise DeliveryError(f"Доставка {delivery.delivery_id} не назначена этому водителю")
        delivery.cancel()


