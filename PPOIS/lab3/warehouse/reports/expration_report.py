from reports.report import Report
from datetime import datetime
class ExpirationReport(Report):
    def __init__(self, warehouse):
        super().__init__(warehouse)

    def generate(self, checker):
        expired = []
        for loc in self.warehouse.locations.values():
            expired.extend(checker.scan_location(loc))
        
        self.data = {
            "checker": checker.full_name(),
            "generated_at": datetime.now().isoformat(),
            "expired_batches": len(expired),
            "details": expired
        }
        return self.data