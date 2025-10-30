from storage.bin import Bin
from enums.bin_type import BinType
from exceptions.errors import *
from enums.product_category import Category
class Shelf(Bin):  
    def __init__(self, code, bin_type, capacity=1000):
        super().__init__(code, bin_type,capacity)

    def receive_batch(self, batch):

        if self.bin_type == BinType.FRIDGE and batch.product.category != Category.FOOD:
            raise WarehouseError(f"Товар {batch.product.name} нельзя в холодильник")
        if self.bin_type == BinType.CHEMICAL and batch.product.category != Category.CHEMICAL:
            raise WarehouseError(f"Товар {batch.product.name} нельзя на хим. полку")
        if self.bin_type == BinType.HAZARD and batch.product.category != Category.HAZARD:
            raise WarehouseError(f"Товар {batch.product.name} нельзя на опасную полку")
        super().receive_batch(batch)
