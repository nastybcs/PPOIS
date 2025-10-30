from exceptions.errors import WarehouseError, EmployeeAlreadyAppointed
from core.employee import Employee

class WarehouseDirector(Employee):
    def __init__(self, first_name,last_name, address,email, warehouse):
        super().__init__(first_name, last_name, address, email,warehouse)
        self.managers = []
    def appoint_manager(self, manager):
        if manager.warehouse != self.warehouse:
            raise WarehouseError (
                f"Менеджер и Директор должны работать на одном складе "
            )
        if manager in self.managers:
            raise EmployeeAlreadyAppointed (
                f"Менеджер {manager.full_name()} уже назначен"
            )
        self.managers.append(manager)
        manager.director = self
        return f"Менеджер {manager.full_name()} уже назначен" 
