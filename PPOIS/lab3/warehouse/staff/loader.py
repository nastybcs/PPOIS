from exceptions.errors import WarehouseError, LocationAlreadyAssigned
from core.employee import Employee
class Loader(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse, manager=None):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.manager = manager
        self.locations = []  
        self.loaded_batches = []

    def assign_location(self, location):
        if location in self.locations:
            raise LocationAlreadyAssigned(f"Локация {location.name} уже закреплена")
        self.locations.append(location)

    def load_batch(self, batch, location):
        if location not in self.locations:
            raise WarehouseError(f"{self.full_name()} не имеет доступа к {location.name}")
        
        bin_obj = location.auto_assign_bin(batch)
        bin_obj.receive_batch(batch)
        self.loaded_batches.append(batch.batch_id)
        
        return f"Грузчик {self.full_name()} загрузил партию {batch.batch_id} в {bin_obj.code}"