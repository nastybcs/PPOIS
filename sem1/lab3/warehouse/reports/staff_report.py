from datetime import datetime
from reports.report import Report

class StaffReport(Report):
    def __init__(self, hr_department):
        super().__init__(hr_department.warehouse)
        self.hr_department = hr_department

    def generate(self):
        self.generated_at = datetime.now()
        self.data= self.hr_department.staff_report()
        return self.data
    
    def total_staff(self):
        if self.data is None:
           self.generate()
        total = 0
        for value in self.data.values():
            if isinstance(value, list):
                total += len(value)
            elif value != "Не назначен":
                total += 1
        return total
