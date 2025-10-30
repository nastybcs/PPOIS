from datetime import datetime
from exceptions.errors import TerminateError
from core.person import Person
class Employee(Person):
    _id_counter = 1

    def __init__(self, first_name, last_name, address, email=None, warehouse=None):
        super().__init__(first_name, last_name, address, email)
        self.employee_id = Employee._id_counter
        Employee._id_counter += 1
        self.hire_date = datetime.now()
        self.is_active = True
        self.warehouse = warehouse

    def terminate(self):
        if not self.is_active:
            raise TerminateError(f"Сотрудник {self.full_name()} уже уволен")
        self.is_active = False
        self.termination_date = datetime.now()

    def info(self):
        return {
            "id": self.employee_id,
            "name": self.full_name(),
            "hire_date": self.hire_date,
            "active": self.is_active,
            "warehouse": getattr(self.warehouse, "name", None)
        }