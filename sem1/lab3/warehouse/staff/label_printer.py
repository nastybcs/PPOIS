from core.employee import Employee
class LabelPrinter(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.printed_labels = 0

    def print_product_label(self, product, quantity=1):
        if quantity <= 0:
            raise ValueError("Количество должно быть > 0")
        
        self.printed_labels += quantity
        return f"Напечатано {quantity} этикеток для '{product.name}' (ID: {product.product_id})"

    def print_batch_label(self, batch):
        self.printed_labels += 1
        return f"Этикетка для партии {batch.batch_id} (товар: {batch.product.name}, {batch.quantity} {batch.product.uom.value})"

    def daily_report(self):
        return f"{self.full_name()}: напечатано {self.printed_labels} этикеток за смену"