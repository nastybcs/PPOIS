from storage.stock import Stock
from exceptions.errors import *
class Bin:
    def __init__(self, code,bin_type, capacity=1000):
        self.code = code
        self.capacity = capacity
        self.bin_type = bin_type
        self.current_load = 0
        self.storage = {} 

    def available_space(self):
        return self.capacity - self.current_load

    def receive_batch(self, batch):
        if batch.quantity > self.available_space():
            raise BinFullError(f"Недостаточно места на полке {self.code}")
        pid = batch.product.product_id
        if pid not in self.storage:
            self.storage[pid] = []
        self.storage[pid].append(batch)
        self.current_load += batch.quantity

    def pick(self, product_id, qty):
        if self.total_qty(product_id) < qty:
            raise InsufficientStockError(f"Недостаточно товара {product_id}")
        picked = 0
        batches = self.storage.get(product_id, [])
        i = 0
        while qty > 0 and i < len(batches):
            batch = batches[i]
            take = min(batch.quantity, qty)
            batch.quantity -= take
            picked += take
            qty -= take
            if batch.quantity == 0:
                i += 1
        self.storage[product_id] = [b for b in batches if b.quantity > 0]
        self.current_load -= picked
        return picked

    def total_qty(self, product_id):
        return sum(b.quantity for b in self.storage.get(product_id, []))