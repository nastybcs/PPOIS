from datetime import datetime
from reports.report import Report
class DeliveryReport(Report):
    def __init__(self, warehouse, hr_department):
        super().__init__(warehouse)
        self.hr = hr_department

    def generate(self):
        self.generated_at = datetime.now()
        report = {}
        for driver in self.hr.drivers:
            report[driver.full_name()] = []
            for delivery in driver.deliveries:
                report[driver.full_name()].append({
                    "order_id": delivery.order.order_id,
                    "status": delivery.status.value,
                    "destination": delivery.destination.full_address()
                })
        self.data = report
        return self.data
    def total_deliveries(self):
        if self.data is None:
            self.generate()
        return sum(len(deliveries) for deliveries in self.data.values())
