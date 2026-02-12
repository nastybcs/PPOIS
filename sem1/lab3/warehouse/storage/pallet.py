from storage.bin import Bin
from exceptions.errors import WarehouseError
from enums.bin_type import BinType
class Pallet(Bin):
    def __init__(self, code, pallet_type=BinType.LARGE_PALLET, capacity=500):
        super().__init__(code, pallet_type, capacity)
        self.stacked = False

    def stack(self):
        if self.stacked:
            raise WarehouseError(f"Паллета {self.code} уже в штабеле")
        self.stacked = True
        self.bin_type = BinType.STACKED_PALLET  

    def receive_batch(self, batch):
        if self.stacked:
            raise WarehouseError(f"Нельзя добавить на штабелированную паллету {self.code}")
        super().receive_batch(batch)