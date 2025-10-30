import unittest
from staff.securityguard import SecurityGuard
from storage.warehouse_module import Warehouse
from exceptions.errors import SecurityGuardNotOnPost


class TestSecurityGuard(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("Test Warehouse")
        self.guard = SecurityGuard(
            first_name="Иван",
            last_name="Сидоров",
            address="Москва, Тверская, 1",
            email="ivan.guard@example.com",
            warehouse=self.warehouse
        )
        self.person = type('Person', (), {'full_name': lambda: "Алексей Петров"})()

    def test_init(self):
        self.assertEqual(self.guard.first_name, "Иван")
        self.assertEqual(self.guard.last_name, "Сидоров")
        self.assertEqual(self.guard.full_name(), "Иван Сидоров")
        self.assertEqual(self.guard.warehouse, self.warehouse)
        self.assertTrue(self.guard.is_active)
        self.assertFalse(self.guard.on_duty)

    def test_start_shift_success(self):
        result = self.guard.start_shift()
        self.assertTrue(self.guard.on_duty)
        self.assertIn("Иван Сидоров", result)
        self.assertIn("на смене", result)

    def test_start_shift_already_on_duty_raises(self):
        self.guard.start_shift()
        with self.assertRaises(SecurityGuardNotOnPost) as cm:
            self.guard.start_shift()
        self.assertIn("уже на смене", str(cm.exception))

    def test_end_shift_success(self):
        self.guard.start_shift()
        result = self.guard.end_shift()
        self.assertFalse(self.guard.on_duty)
        self.assertIn("Иван Сидоров", result)
        self.assertIn("смена завершена", result)

    def test_end_shift_not_on_duty_raises(self):
        with self.assertRaises(SecurityGuardNotOnPost) as cm:
            self.guard.end_shift()
        self.assertIn("не на смене", str(cm.exception))

    def test_check_access_when_on_duty(self):
        self.guard.start_shift()
        result = self.guard.check_access(self.person)
        self.assertTrue(result)

    def test_check_access_when_not_on_duty_raises(self):
        with self.assertRaises(SecurityGuardNotOnPost) as cm:
            self.guard.check_access(self.person)
        self.assertIn("Охранник не на посту!", str(cm.exception))

    def test_check_access_after_termination(self):
        self.guard.terminate()
        with self.assertRaises(SecurityGuardNotOnPost):
            self.guard.check_access(self.person)
        self.guard.start_shift() 
        self.assertTrue(self.guard.on_duty)
        self.assertTrue(self.guard.check_access(self.person))

    def test_multiple_shift_cycles(self):
        self.guard.start_shift()
        self.guard.end_shift()
        self.guard.start_shift()
        self.assertTrue(self.guard.on_duty)
        with self.assertRaises(SecurityGuardNotOnPost):
            self.guard.start_shift()

    def test_check_access_with_different_person(self):
        self.guard.start_shift()
        person2 = type('Person', (), {'full_name': lambda: "Мария Козлова"})()
        result = self.guard.check_access(person2)
        self.assertTrue(result)

