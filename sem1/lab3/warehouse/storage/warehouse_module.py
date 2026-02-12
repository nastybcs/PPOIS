from exceptions.errors import *
from storage.expired_bin import ExpiredBin
class Warehouse:
    def __init__(self, name):
        self.name = name
        self.products = {}      
        self.locations = {}     
        self.expired_bin = ExpiredBin(self)
    def register_product(self, product):
        if product.product_id in self.products:
            raise WarehouseError(f"Товар {product.product_id} уже зарегистрирован")
        self.products[product.product_id] = product

    def add_location(self, location):
        if location.name in self.locations:
            raise WarehouseError(f"Локация {location.name} уже существует")
        self.locations[location.name] = location

    def stock_report(self):

        report = {}
        for pid in self.products:
            total = sum(loc.total_qty(pid) for loc in self.locations.values())
            report[pid] = total
        return report

    def total_qty(self, product_id):
        return sum(loc.total_qty(product_id) for loc in self.locations.values())