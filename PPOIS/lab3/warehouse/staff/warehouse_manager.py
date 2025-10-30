from core.employee import Employee 
from exceptions.errors import *
from enums.order_status import OrderStatus
class WarehouseManager(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.director = None
        self.storekeepers = []
        self.managed_orders = [] 
        self.loaders = []

    def info(self):
       data = super().info()
       data["director"] = self.director.full_name() if self.director else None
       return data

        
    def appoint_storekeeper(self, storekeeper):
        if self.warehouse != storekeeper.warehouse:
            raise WarehouseError (
                f"Кладовщик и Менеджер должны работать на одном складе"
            )
        if storekeeper in self.storekeepers:
            raise EmployeeAlreadyAppointed (
                f"Кладовщик {storekeeper.full_name()} уже назначен"
            )
        self.storekeepers.append(storekeeper)
        storekeeper.manager = self
        return f"Кладовщик {storekeeper.full_name()} уже назначен"
    def register_order(self, order):
        self.managed_orders.append(order)
        return order

    def assign_storekeeper(self, order, storekeeper):
        if order.status != OrderStatus.CREATED:
            raise OrderAlreadyExist(f"Заказ {order.order_id} уже в обработке")
        if storekeeper not in self.storekeepers:
            raise WarehouseError(f"{storekeeper.full_name()} не работает у этого менеджера")
        storekeeper.pick_order(order)
        order.status = OrderStatus.READY
        return f"Заказ {order.order_id} собран кладовщиком {storekeeper.full_name()}"
    
    def appoint_loader(self, loader):
        if self.warehouse != loader.warehouse:
            raise WarehouseError("Грузчик должен быть на этом складе")
        if loader in self.loaders:
            raise EmployeeAlreadyAppointed(f"Грузчик {loader.full_name()} уже назначен")
        self.loaders.append(loader)
        loader.manager = self
        return f"Грузчик {loader.full_name()} уже назначен"

    def assign_loader_location(self, loader, location):
        if loader not in self.loaders:
            raise WarehouseError(f"{loader.full_name()} не под вашим управлением")
        loader.assign_location(location)

    def order_status(self, order):

        return order.status

    def total_orders(self):
        return len(self.managed_orders)