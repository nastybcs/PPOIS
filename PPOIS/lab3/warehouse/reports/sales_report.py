from datetime import datetime
from reports.report import Report
class SalesReport(Report):
    def __init__(self, warehouse, aggregator):
        super().__init__(warehouse)
        self.aggregator = aggregator

    def generate(self):
        self.generated_at = datetime.now()
        self.data = self.aggregator.get_report(self.warehouse)
        return self.data

    def total_sales(self):
        return self.aggregator.total_sales(self.warehouse)
