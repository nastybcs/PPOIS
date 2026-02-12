from enums.route_status import RouteStatus
from exceptions.errors import DeliveryError
from datetime import datetime
class Route:

    _id_counter = 1

    def __init__(self, driver, vehicle):
        self.route_id = Route._id_counter   
        Route._id_counter += 1

        self.driver = driver
        self.vehicle = vehicle
        self.points = []
        self.status = RouteStatus.PLANNED
        self.started_at = None
        self.completed_at = None

    def add_point(self, route_point):
        if self.status != RouteStatus.PLANNED:
            raise DeliveryError("Нельзя добавлять точки после начала маршрута")
        self.points.append(route_point)

    def start(self):
        if self.status != RouteStatus.PLANNED:
            raise DeliveryError("Маршрут уже начат или отменён")
        if not self.points:
            raise DeliveryError("Нельзя начать маршрут без точек")
        self.status = RouteStatus.IN_PROGRESS
        self.started_at = datetime.now()

    def mark_point_visited(self, index):
        if self.status != RouteStatus.IN_PROGRESS:
            raise DeliveryError("Маршрут не находится в пути")
        try:
            point = self.points[index]
            point.mark_visited()
        except IndexError:
            raise DeliveryError(f"Точка {index} не найдена")

    def complete(self):
        if self.status != RouteStatus.IN_PROGRESS:
            raise DeliveryError("Нельзя завершить неактивный маршрут")
        if not all(p.visited for p in self.points):
            raise DeliveryError("Не все точки маршрута посещены")
        self.status = RouteStatus.COMPLETED
        self.completed_at = datetime.now()

    def cancel(self):
        if self.status == RouteStatus.COMPLETED:
            raise DeliveryError("Нельзя отменить завершённый маршрут")
        self.status = RouteStatus.CANCELLED

    def info(self):
        return {
            "route_id": self.route_id,
            "driver": self.driver.full_name(),
            "vehicle": str(self.vehicle),
            "points_total": len(self.points),
            "visited": sum(1 for p in self.points if p.visited),
            "status": self.status.value,
        }