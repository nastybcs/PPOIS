class WarehouseChecker:
    def __init__(self, warehouse):
        self.warehouse = warehouse
    def quick_check(self):
        return f"Склад: {len(self.warehouse.products)} товаров, {len(self.warehouse.locations)} локаций"