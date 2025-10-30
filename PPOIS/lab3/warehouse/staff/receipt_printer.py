from datetime import datetime
from core.employee import Employee
from enums.order_status import OrderStatus
class ReceiptPrinter(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.printed_receipts = 0

    def print_receipt(self, order):
        if order.status != OrderStatus.DELIVERED:
            raise ValueError("Чек можно печатать только для доставленного заказа")
        
        self.printed_receipts += 1
        total = order.total_amount()
        items = "\n".join([f"  {item.product.name} x{item.quantity} = {item.total_price()} руб."
                          for item in order.items])
        
        receipt = f"""
=== ЧЕК #{self.printed_receipts} ===
Заказ: {order.order_id}
Клиент: {order.customer.full_name()}
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

{items}

ИТОГО: {total} руб.
Спасибо за покупку!
===============================
"""
        return receipt.strip()