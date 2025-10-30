from core.employee import Employee
from storage.pallet import Pallet
from exceptions.errors import WarehouseError
class PalletWrapper(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.wrapped_pallets = 0

    def wrap_pallet(self, pallet):
        if not isinstance(pallet, Pallet):
            raise ValueError("Можно оборачивать только паллеты")
        if pallet.stacked:
            raise WarehouseError(f"Паллета {pallet.code} уже в штабеле")
        
        self.wrapped_pallets += 1
        return f"Паллета {pallet.code} обёрнута плёнкой сотрудником {self.full_name()}"