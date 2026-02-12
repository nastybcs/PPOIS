import unittest
from datetime import datetime
from exceptions.errors import NoOrderManagerError
from staff.accountant import Accountant
from storage.warehouse_module import Warehouse
from staff.order_manager import OrderManager
from staff.order_manager import OrderManager
from staff.order_manager import OrderManager  
from staff.order_manager import OrderManager  

class TestAccountantReal(unittest.TestCase):
    def setUp(self):
        
        self.warehouse = Warehouse("Склад-тест")
        self.order_manager = OrderManager("Олег", "Смирнов", "Адрес", "oleg@example.com", self.warehouse)
        self.hr = type("HRStub", (), {})()
        self.hr.order_managers = [self.order_manager]
        self.accountant = Accountant("Ирина", "Попова", "Город", "irina@example.com", self.warehouse, self.hr)

    def test_get_aggregator_success(self):
        agg = self.accountant._get_aggregator()
        self.assertIs(agg, self.order_manager.sales_aggregator)

    def test_get_aggregator_no_order_manager_raises(self):
        self.hr.order_managers = []
        with self.assertRaises(NoOrderManagerError):
            self.accountant._get_aggregator()

    def test_generate_sales_report_returns_dict_and_logs(self):
        data = self.accountant.generate_sales_report()
        self.assertIsInstance(data, dict)
        self.assertTrue(self.accountant.reports_generated)
        name, timestamp = self.accountant.reports_generated[-1]
        self.assertEqual(name, "Продажи")
        self.assertIsInstance(timestamp, datetime)

    def test_generate_profit_report_when_data_present(self):
    
        result = self.accountant.generate_profit_report()
        self.assertIn("total_profit", result)
        self.assertEqual(self.accountant.reports_generated[-1][0], "Прибыль")

    def test_generate_tax_report_computes_correctly(self):
        result = self.accountant.generate_tax_report()
        self.assertIn("total_tax", result)
        self.assertEqual(self.accountant.reports_generated[-1][0], "Налоги")

    def test_reports_generated_order(self):
        self.accountant.generate_sales_report()
        self.accountant.generate_profit_report()
        self.accountant.generate_tax_report()
        types = [entry[0] for entry in self.accountant.reports_generated]
        self.assertEqual(types, ["Продажи", "Прибыль", "Налоги"])

