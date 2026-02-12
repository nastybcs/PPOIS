from enums.uom import UOM
from enums.product_category import Category
class Product:
    def __init__(self,name, product_id, price,weight = None,category= Category.OTHER, uom = UOM.PIECE):
        self.name = name 
        self.product_id = product_id
        self.category = category
        self.weight = weight
        self.price = price
        self.uom = uom
    def summary(self):
        return f"{self.name} ({self.product_id}) - {self.category.value}, {self.price} руб. за {self.uom.value}"