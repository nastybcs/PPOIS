from core.employee import Employee
from datetime import datetime
from reports.sales_report import SalesReport
from exceptions.errors import NoOrderManagerError

class Accountant(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse, hr):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.hr = hr
        self.reports_generated = []

    def _get_aggregator(self):
        if not self.hr.order_managers:
            raise NoOrderManagerError("Нет менеджеров заказов")
        return self.hr.order_managers[0].sales_aggregator

    def generate_sales_report(self):
        report = SalesReport(self.warehouse, self._get_aggregator())
        data = report.generate()
        self.reports_generated.append(("Продажи", datetime.now()))
        return data

    def generate_profit_report(self):
        report = SalesReport(self.warehouse, self._get_aggregator())
        sales = report.generate()
        total_profit = sum(item["total_amount"] for item in sales.values())
        self.reports_generated.append(("Прибыль", datetime.now()))
        return {"total_profit": total_profit}

    def generate_tax_report(self):
        report = SalesReport(self.warehouse, self._get_aggregator())
        sales = report.generate()
        tax = sum(item["total_amount"] * 0.20 for item in sales.values())
        self.reports_generated.append(("Налоги", datetime.now()))
        return {"total_tax": tax}