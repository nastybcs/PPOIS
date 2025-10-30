import unittest
from datetime import datetime

from reports.staff_report import StaffReport
from storage.warehouse_module import Warehouse
from staff.department import HRDepartment

class TestStaffReport(unittest.TestCase):

    def setUp(self):
      

        self.warehouse = Warehouse("Test Warehouse")
        self.hr = HRDepartment(self.warehouse)

       
        self.director = self.hr.appoint_director("Ivan", "Ivanov", "Moscow", "dir@wh")
        self.manager = self.hr.hire_manager("Anna", "Petrova", "SPb", "mgr@wh")
        self.driver = self.hr.hire_driver("Max", "Sidorov", "Kazan", "drv@wh", "A123BC")
        self.storekeeper = self.hr.hire_storekeeper("Oleg", "Kuznetsov", "NN", "sk@wh")
        self.checker = self.hr.hire_expiration_checker("Lena", "Smirnova", "EKB", "exp@wh")


        self.report = StaffReport(self.hr)

    def test_init_sets_hr_department(self):
        self.assertEqual(self.report.hr_department, self.hr)
        self.assertIsNone(self.report.data)



    def test_generate_calls_staff_report_and_sets_data(self):
        data = self.report.generate()

        self.assertIsInstance(self.report.generated_at, datetime)
        self.assertEqual(data, self.report.data)

        self.assertEqual(data["Директор"], "Ivan Ivanov")
        self.assertIn("Anna Petrova", data["Менеджеры"])
        self.assertIn("Max Sidorov", data["Водители"])
        self.assertIn("Oleg Kuznetsov", data["Кладовщики"])
        self.assertIn("Lena Smirnova", data["Контролёры просрочки"])

    def test_generate_empty_if_no_staff(self):
        empty_hr = HRDepartment(self.warehouse)
        report = StaffReport(empty_hr)
        data = report.generate()

        self.assertEqual(data["Директор"], "Не назначен")
        for key in data:
            if isinstance(data[key], list):
                self.assertEqual(data[key], [])
            else:
                self.assertEqual(data[key], "Не назначен")

    def test_total_staff_counts_all_employees(self):
        self.report.generate()
        total = self.report.total_staff()
        self.assertEqual(total, 5) 

    def test_total_staff_calls_generate_if_no_data(self):
        self.assertIsNone(self.report.data)
        total = self.report.total_staff()
        self.assertEqual(total, 5)
        self.assertIsNotNone(self.report.data)

    def test_total_staff_zero_if_empty(self):
        empty_hr = HRDepartment(self.warehouse)
        report = StaffReport(empty_hr)
        self.assertEqual(report.total_staff(), 0)
