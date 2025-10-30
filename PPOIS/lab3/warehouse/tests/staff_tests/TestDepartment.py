import unittest
from staff.department import HRDepartment
from staff.warehouse_director import WarehouseDirector
from storage.warehouse_module import Warehouse
from exceptions.errors import NoChiefForEmployee, EmployeeAlreadyAppointed


class TestHRDepartment(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Main Warehouse")
        self.hr = HRDepartment(self.warehouse)

    def test_appoint_director_and_hire_manager(self):
        director = self.hr.appoint_director("Dir", "Test", "City, St, 1", "dir@test.com")
        self.assertIsInstance(director, WarehouseDirector)
        self.assertEqual(self.hr.director, director)
        manager = self.hr.hire_manager("Man", "Test", "City, St, 2", "man@test.com")
        self.assertIn(manager, self.hr.managers)
        self.assertEqual(manager.director, director)


        with self.assertRaises(EmployeeAlreadyAppointed):
            self.hr.appoint_director("Dir2", "Test2", "City, St, 3", "dir2@test.com")

        self.hr.director = None
        with self.assertRaises(NoChiefForEmployee):
            self.hr.hire_manager("Man2", "Test2", "City, St, 3", "man2@test.com")

    def test_hire_various_employees(self):
        director = self.hr.appoint_director("Dir", "Test", "City, St, 1", "dir@test.com")
        manager = self.hr.hire_manager("Man", "Test", "City, St, 2", "man@test.com")

        storekeeper = self.hr.hire_storekeeper("Store", "Keeper", "City, St, 3", "store@test.com", manager)
        loader = self.hr.hire_loader("Load", "Er", "City, St, 4", "loader@test.com", manager)
        guard = self.hr.hire_security_guard("Sec", "Guard", "City, St, 5", "sec@test.com")
        cleaner = self.hr.hire_cleaner("Clean", "Er", "City, St, 6", "clean@test.com")
        driver = self.hr.hire_driver("Drive", "Er", "City, St, 7", "driver@test.com", "ABC123")
        accountant = self.hr.hire_accountant("Acc", "Ountant", "City, St, 8", "acc@test.com")
        order_manager = self.hr.hire_order_manager("Order", "Man", "City, St, 9", "om@test.com")
        expiration_checker = self.hr.hire_expiration_checker("Exp", "Checker", "City, St, 10", "exp@test.com")
        label_printer = self.hr.hire_label_printer("Label", "Print", "City, St, 11", "label@test.com")
        receipt_printer = self.hr.hire_receipt_printer("Receipt", "Print", "City, St, 12", "receipt@test.com")
        pallet_wrapper = self.hr.hire_pallet_wrapper("Pallet", "Wrap", "City, St, 13", "pallet@test.com")

        self.assertIn(storekeeper, self.hr.storekeepers)
        self.assertIn(loader, self.hr.loaders)
        self.assertIn(guard, self.hr.security_guards)
        self.assertIn(cleaner, self.hr.cleaners)
        self.assertIn(driver, self.hr.drivers)
        self.assertIn(accountant, self.hr.accountants)
        self.assertIn(order_manager, self.hr.order_managers)
        self.assertIn(expiration_checker, self.hr.expiration_checkers)
        self.assertIn(label_printer, self.hr.label_printers)
        self.assertIn(receipt_printer, self.hr.receipt_printers)
        self.assertIn(pallet_wrapper, self.hr.pallet_wrappers)

    def test_fire_employee_and_cleanup(self):
        director = self.hr.appoint_director("Dir", "Test", "City, St, 1", "dir@test.com")
        manager = self.hr.hire_manager("Man", "Test", "City, St, 2", "man@test.com")
        storekeeper = self.hr.hire_storekeeper("Store", "Keeper", "City, St, 3", "store@test.com", manager)
        loader = self.hr.hire_loader("Load", "Er", "City, St, 4", "loader@test.com", manager)
        driver = self.hr.hire_driver("Drive", "Er", "City, St, 7", "driver@test.com", "ABC123")

        self.hr.fire_employee(manager)
        self.assertNotIn(manager, self.hr.managers)
        self.assertIsNone(manager.director)

        self.hr.fire_employee(storekeeper)
        self.assertNotIn(storekeeper, self.hr.storekeepers)

        self.hr.fire_employee(loader)
        self.assertNotIn(loader, self.hr.loaders)

        self.hr.fire_employee(driver)
        self.assertNotIn(driver, self.hr.drivers)

    def test_staff_report_accuracy(self):
        director = self.hr.appoint_director("Dir", "Test", "City, St, 1", "dir@test.com")
        manager = self.hr.hire_manager("Man", "Test", "City, St, 2", "man@test.com")
        storekeeper = self.hr.hire_storekeeper("Store", "Keeper", "City, St, 3", "store@test.com", manager)

        report = self.hr.staff_report()
        self.assertEqual(report["Директор"], director.full_name())
        self.assertIn(manager.full_name(), report["Менеджеры"])
        self.assertIn(storekeeper.full_name(), report["Кладовщики"])
