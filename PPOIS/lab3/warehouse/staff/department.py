from exceptions.errors import *
from staff.warehouse_director import WarehouseDirector
from staff.warehouse_manager import WarehouseManager
from staff.cleaner import Cleaner
from staff.driver import Driver
from staff.securityguard import SecurityGuard
from staff.storekeeper import Storekeeper
from staff.accountant import Accountant
from orders.customer import Customer
from staff.order_manager import OrderManager
from staff.expiration_checker import ExpirationChecker
from staff.loader import Loader
from staff.label_printer import LabelPrinter
from staff.pallet_wrapper import PalletWrapper
from staff.receipt_printer import ReceiptPrinter


class HRDepartment:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.director = None
        self.managers = []
        self.storekeepers = []
        self.security_guards = []
        self.cleaners = []
        self.drivers = []
        self.accountants = []
        self.customers = []
        self.order_managers = []
        self.expiration_checkers = []
        self.loaders = [] 
        self.label_printers = []
        self.receipt_printers = []
        self.pallet_wrappers = []

    def hire_loader(self, first_name, last_name, address, email=None, manager=None):
        if not self.managers and not manager:
            raise NoChiefForEmployee("Нет менеджера для грузчика")
        if manager is None:
            manager = self.managers[0]
        
        loader = Loader(first_name, last_name, address, email, self.warehouse, manager)
        manager.appoint_loader(loader)
        self.loaders.append(loader)
        return loader
    def hire_label_printer(self, first_name, last_name, address, email=None):
        printer = LabelPrinter(first_name, last_name, address, email, self.warehouse)
        self.label_printers.append(printer)
        return printer

    def appoint_director(self, first_name, last_name, address, email):
        if self.director:
            raise EmployeeAlreadyAppointed("Директор уже назначен")
        director = WarehouseDirector(first_name, last_name, address, email, self.warehouse)
        self.director = director
        return director
    def register_customer(self, first_name, last_name, address, email=None):
        customer = Customer(first_name, last_name, address, email)
        self.customers.append(customer)
        return customer
    def hire_order_manager(self, first_name, last_name, address, email):
        manager = OrderManager(first_name, last_name, address, email, self.warehouse)
        self.order_managers = getattr(self, 'order_managers', [])  
        self.order_managers.append(manager)
        return manager
    def hire_receipt_printer(self, first_name, last_name, address, email=None):
        printer = ReceiptPrinter(first_name, last_name, address, email, self.warehouse)
        self.receipt_printers.append(printer)
        return printer

    def hire_pallet_wrapper(self, first_name, last_name, address, email=None):
        wrapper = PalletWrapper(first_name, last_name, address, email, self.warehouse)
        self.pallet_wrappers.append(wrapper)
        return wrapper
    def hire_expiration_checker(self, first_name, last_name, address, email=None):
        checker = ExpirationChecker(first_name, last_name, address, email, self.warehouse)
        self.expiration_checkers.append(checker)
        return checker

    def hire_manager(self, first_name, last_name, address, email):
        if not self.director:
            raise  NoChiefForEmployee("Нельзя назначить менеджера без директора")
        manager = WarehouseManager(first_name, last_name, address, email, self.warehouse)
        self.director.appoint_manager(manager)
        self.managers.append(manager)
        return manager

    def hire_storekeeper(self, first_name, last_name, address, email, manager=None):
        if not self.managers and not manager:
            raise NoChiefForEmployee("Нет менеджеров для назначения кладовщика")
        if manager is None:
            manager = self.managers[0]
        storekeeper = Storekeeper(first_name, last_name, address, email, self.warehouse, manager)
        manager.appoint_storekeeper(storekeeper)
        self.storekeepers.append(storekeeper)
        return storekeeper

    def hire_security_guard(self, first_name, last_name, address, email):
        guard = SecurityGuard(first_name, last_name, address, email, self.warehouse)
        self.security_guards.append(guard)
        return guard

    def hire_cleaner(self, first_name, last_name, address, email):
        cleaner = Cleaner(first_name, last_name, address, email, self.warehouse)
        self.cleaners.append(cleaner)
        return cleaner

    def hire_driver(self, first_name, last_name, address, email, vehicle_number):
        driver = Driver(first_name, last_name, address, email, self.warehouse, vehicle_number)
        self.drivers.append(driver)
        return driver
    def hire_accountant(self, first_name, last_name, address, email):
        accountant = Accountant(first_name, last_name, address, email, self.warehouse,self)
        self.accountants.append(accountant)
        return accountant

    def fire_employee(self, person):
        person.terminate()

        if isinstance(person, WarehouseDirector) and self.director == person:
            self.director = None
            for m in self.managers:
                m.director = None

        if isinstance(person, WarehouseManager):

            for s in getattr(person, "storekeepers", []):
                s.manager = None
  
            person.director = None
   
            if person in self.managers:
                self.managers.remove(person)

        if isinstance(person, Storekeeper) and person in self.storekeepers:
            self.storekeepers.remove(person)
        if isinstance(person, Loader) and person in self.loaders:
            self.loaders.remove(person)

        if isinstance(person, Accountant) and person in self.accountants:
            self.accountants.remove(person)
        if isinstance(person, OrderManager) and person in self.order_managers:
            self.order_managers.remove(person)
        if isinstance(person, ExpirationChecker) and person in self.expiration_checkers:
            self.expiration_checkers.remove(person)
        if isinstance(person, LabelPrinter) and person in self.label_printers:
            self.label_printers.remove(person)
        if isinstance(person, ReceiptPrinter) and person in self.receipt_printers:
            self.receipt_printers.remove(person)
        if isinstance(person, PalletWrapper) and person in self.pallet_wrappers:
            self.pallet_wrappers.remove(person)

        for group in [self.security_guards, self.cleaners, self.drivers]:
            if person in group:
                group.remove(person)

    def staff_report(self):
        return {
            "Директор": self.director.full_name() if self.director else "Не назначен",
            "Менеджеры": [m.full_name() for m in self.managers],
            "Менеджеры заказов": [om.full_name() for om in self.order_managers],
            "Кладовщики": [s.full_name() for s in self.storekeepers],
            "Охрана": [g.full_name() for g in self.security_guards],
            "Уборщики": [c.full_name() for c in self.cleaners],
            "Водители": [d.full_name() for d in self.drivers],
            "Бухгалтеры": [a.full_name() for a in self.accountants],
            "Контролёры просрочки": [ec.full_name() for ec in self.expiration_checkers],
            "Грузчики": [l.full_name() for l in self.loaders],
            "Принтеры этикеток": [p.full_name() for p in self.label_printers],
            "Принтеры чеков": [p.full_name() for p in self.receipt_printers],
            "Обмотчики паллет": [w.full_name() for w in self.pallet_wrappers],
        }