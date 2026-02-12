from exceptions.errors import *
from enums.bin_type import BinType
from enums.product_category import Category
from datetime import date


class Location:
    def __init__(self, name):
        self.name = name
        self.bins = {}  

    def add_bin(self, bin_obj): 
        if bin_obj.code in self.bins:
            raise WarehouseError(f"Ячейка {bin_obj.code} уже есть")
        self.bins[bin_obj.code] = bin_obj

    def get_bins(self, code):
        if code not in self.bins:
            raise WarehouseError(f"Полка {code} не найдена")
        return self.bins[code]

    def total_qty(self, product_id):
        return sum(s.total_qty(product_id) for s in self.bins.values())

    def _earliest_expiration_in_bin(self, bin_obj, product_id):
        batches = bin_obj.storage.get(product_id, [])
        dates = [b.exp_date for b in batches if b.exp_date]
        return min(dates) if dates else date.max
    def _find_best_bin_by_expiration(self, candidates, product_id):
        if not candidates:
            return None

        best_bin = candidates[0]
        earliest_date = self._earliest_expiration_in_bin(best_bin, product_id)

        for bin_obj in candidates[1:]:
            current_date = self._earliest_expiration_in_bin(bin_obj, product_id)
            if current_date < earliest_date:
                earliest_date = current_date
                best_bin = bin_obj

        return best_bin

    def auto_assign_bin(self, batch):
        candidates = []
        for bin_obj in self.bins.values():
            if bin_obj.available_space() < batch.quantity:
                continue

            if bin_obj.bin_type in [BinType.FRIDGE, BinType.CHEMICAL, BinType.HAZARD]:
                if bin_obj.bin_type == BinType.FRIDGE and batch.product.category != Category.FOOD:
                    continue
                if bin_obj.bin_type == BinType.CHEMICAL and batch.product.category != Category.CHEMICAL:
                    continue
                if bin_obj.bin_type == BinType.HAZARD and batch.product.category != Category.HAZARD:
                    continue

            if bin_obj.bin_type in [BinType.SEALED_BOX, BinType.STACKED_PALLET]:
                continue

            candidates.append(bin_obj)

        if not candidates:
            raise WarehouseError(f"Нет места для {batch.product.name}")

        best_bin = self._find_best_bin_by_expiration(candidates, batch.product.product_id)
        return best_bin
