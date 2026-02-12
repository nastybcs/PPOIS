from exceptions.errors import *

class Stock:
    def __init__(self):
        self.storage = {}
    def receive(self, batch):
        pid = batch.product.product_id
        if pid not in self.storage:
            self.storage[pid]=[]
        if any(b.batch_id == batch.batch_id for b in self.storage[pid]):
            raise BatchError(f"Партия {batch.batch_id} уже принята")
        self.storage[pid].append(batch)
    def total_qty(self, product_id):
        return sum(b.quantity for b in self.storage.get(product_id,[]))
    
    def pick (self,product_id, quantity):
        if self.total_qty(product_id) < quantity:
            raise InsufficientStockError(f"Недостаточно товара {product_id}")
        picked = 0
        batches = self.storage.get(product_id, [])
        i = 0
        while quantity > 0 and i < len(batches):
            batch = batches[i]
            take = min(batch.quantity, quantity)
            batch.quantity -= take
            picked += take
            quantity -= take
            if batch.quantity == 0:
                i += 1
        self.storage[product_id] = [b for b in batches if b.quantity > 0]
        return picked
