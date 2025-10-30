from core.employee import Employee
from exceptions.errors import *
from enums.order_status import OrderStatus

class Storekeeper(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse, manager = None):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.locations = []
        self.manager = manager

    def assign_location(self, location):
        if location in self.locations:
            raise LocationAlreadyAssigned(f"Локация {location.name} уже закреплена за {self.full_name()}")
        self.locations.append(location)

    def receive_batch(self, loc_obj, batch):
        if loc_obj not in self.locations:
            raise WarehouseError(f"{self.full_name()} нет доступа к {loc_obj.name}")
        bin_obj = loc_obj.auto_assign_bin(batch)
        bin_obj.receive_batch(batch)

    def pick(self, loc_obj, shelf_obj, product, qty):
        if loc_obj not in self.locations:
            raise WarehouseError(f"{self.full_name()} не имеет доступа к {loc_obj.name}")
        shelf_ref = loc_obj.get_bins(shelf_obj.code)
        return shelf_ref.pick(product.product_id, qty)
    
    def pick_order(self, order):
        if order.status != OrderStatus.CREATED:
            raise ValueError("Заказ уже в обработке")
    
        order.status = OrderStatus.PICKING  
        for item in order.items:
            total_picked = 0
            for loc in self.locations:
                for bin_obj in loc.bins.values():
                    if total_picked >= item.quantity:
                        break
                    available = bin_obj.total_qty(item.product.product_id)
                    if available > 0:
                        need = item.quantity - total_picked
                        take = min(need, available)
                        bin_obj.pick(item.product.product_id, take)
                        total_picked += take
                if total_picked < item.quantity:
                    raise InsufficientStockError(f"Недостаточно {item.product.name}")
    
        order.status = OrderStatus.READY  
        return True   

    def total_qty(self, product):
        return sum(loc.total_qty(product.product_id) for loc in self.locations)
