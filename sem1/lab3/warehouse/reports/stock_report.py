from datetime import datetime
from reports.report import Report
class StockReport(Report):
    def generate(self):
        self.generated_at = datetime.now()
        self.data = {}
        for pid, product in self.warehouse.products.items():
            total = self.warehouse.total_qty(pid)
            self.data[product.name] = total
        return self.data
    
    def total_items(self):
        if not self.data:
            self.generate()
        return sum(self.data.values())