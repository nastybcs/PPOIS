from datetime import datetime

class ExpiredBin:
    def __init__(self, warehouse, code="EXPIRED-01"):
        self.code = code
        self.warehouse = warehouse
        self.batches = [] 
        self.total_qty = 0

    def add_expired_batch(self, batch, checker):
        if not batch.is_expired():
            raise ValueError("Партия не просрочена!")
        
        self.batches.append({
            "batch": batch,
            "moved_by": checker.full_name(),
            "moved_at": datetime.now()
        })
        self.total_qty += batch.quantity

        return f"Партия {batch.batch_id} перемещена в корзину просрочки"

    def clear(self, accountant):
        if not self.batches:
            return "Корзина пуста"
        cleared = len(self.batches)
        self.batches = []
        self.total_qty = 0
        return f"Корзина очищена бухгалтером {accountant.full_name()}, списано {cleared} партий"

    def report(self):
        return {
            "code": self.code,
            "total_batches": len(self.batches),
            "total_qty": self.total_qty,
            "contents": [
                {
                    "product": b["batch"].product.name,
                    "batch_id": b["batch"].batch_id,
                    "qty": b["batch"].quantity,
                    "exp_date": b["batch"].exp_date,
                    "moved_by": b["moved_by"]
                }
                for b in self.batches
            ]
        }