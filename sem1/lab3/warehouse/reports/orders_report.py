from datetime import datetime
from reports.report import Report
class OrdersReport(Report):
    def generate(self):
        self.generated_at = datetime.now()
        self.data = {}

        for loc in self.warehouse.locations.values():
            for bin_obj in loc.bins.values():
                for batches in bin_obj.storage.values():
                    self._accumulate_batches(batches)

        return self.data
    def _accumulate_batches(self, batches):
        for batch in batches:
            name = batch.product.name
            self.data[name] = self.data.get(name, 0) + batch.quantity

    def total_quantity(self):
        if not getattr(self, "data", None):
            self.generate()
        return sum(self.data.values())
