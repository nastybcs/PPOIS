from storage.bin import Bin
from exceptions.errors import WarehouseError
from enums.bin_type import BinType
class Box(Bin):
    def __init__(self, code, box_type=BinType.SMALL_BOX, capacity=50):
        super().__init__(code, box_type, capacity)
        self.sealed = False

    def seal(self):
        if self.sealed:
            raise WarehouseError(f"Коробка {self.code} уже запечатана")
        self.sealed = True
        self.bin_type = BinType.SEALED_BOX  

    def receive_batch(self, batch):
        if self.sealed:
            raise WarehouseError(f"Нельзя добавить в запечатанную коробку {self.code}")
        super().receive_batch(batch)