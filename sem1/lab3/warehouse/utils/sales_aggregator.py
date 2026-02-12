from enums.order_status import OrderStatus
class SalesAggregator:
    def __init__(self):
        self.sales_by_product = {}  

    def record_delivery(self, order):

        if order.status != OrderStatus.DELIVERED:
            return
        for item in order.items:
            pid = item.product.product_id
            if pid not in self.sales_by_product:
                self.sales_by_product[pid] = {"qty": 0, "amount": 0}
            self.sales_by_product[pid]["qty"] += item.quantity
            self.sales_by_product[pid]["amount"] += item.total_price()

    def get_report(self, warehouse):
        report = {}
        for pid, data in self.sales_by_product.items():
            product = warehouse.products.get(pid)
            if product:
                report[product.name] = {
                    "sold_qty": data["qty"],
                    "total_amount": data["amount"]
                }
        return report

    def total_sales(self, warehouse):
        report = self.get_report(warehouse)
        return sum(item["total_amount"] for item in report.values())