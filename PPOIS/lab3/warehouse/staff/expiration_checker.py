from core.employee import Employee
from exceptions.errors import WarehouseError
class ExpirationChecker(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.checked_batches = []  
    def scan_location(self, location):
        expired = []
        for bin_obj in location.bins.values():
            for batches in bin_obj.storage.values():
                for batch in batches:
                    if batch.is_expired():
                        expired.append({
                            "product": batch.product.name,
                            "batch_id": batch.batch_id,
                            "exp_date": batch.exp_date,
                            "qty": batch.quantity
                        })
                        self.checked_batches.append(batch)
        return expired

    def full_report(self):
        total = len([b for b in self.checked_batches if b.is_expired()])
        return f"{self.full_name()}: найдено {total} просроченных партий"
    def move_to_expired_bin(self, batch, expired_bin):
        if batch not in self.checked_batches:
  
            found = False
            for loc in self.warehouse.locations.values():
                for bin_obj in loc.bins.values():
                    if batch in [b for batches in bin_obj.storage.values() for b in batches]:
                        found = True
                        break
                if found:
                    break
            if not found:
                raise WarehouseError("Партия не найдена на складе")

        if not batch.is_expired():
            raise WarehouseError("Партия не просрочена")

  
        for loc in self.warehouse.locations.values():
            for bin_obj in loc.bins.values():
                if batch in [b for batches in bin_obj.storage.values() for b in batches]:
                    bin_obj.pick(batch.product.product_id, batch.quantity)
                    break

        return expired_bin.add_expired_batch(batch, self)