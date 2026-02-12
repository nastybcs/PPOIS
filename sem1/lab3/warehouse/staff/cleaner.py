from core.employee import Employee
from datetime import datetime
class Cleaner(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.locations_cleaned = []

    def clean_location(self, location):
        self.locations_cleaned.append((location.name, datetime.now()))
        return f"Локация {location.name} очищена уборщиком {self.full_name()}"
