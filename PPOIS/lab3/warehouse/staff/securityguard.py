from core.employee import Employee
from exceptions.errors import SecurityGuardNotOnPost

class SecurityGuard(Employee):
    def __init__(self, first_name, last_name, address, email, warehouse):
        super().__init__(first_name, last_name, address, email, warehouse)
        self.on_duty = False

    def start_shift(self):
        if self.on_duty:
            raise SecurityGuardNotOnPost(f"Охранник {self.full_name()} уже на смене")
        self.on_duty = True
        return f"{self.full_name()} теперь на смене"

    def end_shift(self):
        if not self.on_duty:
            raise SecurityGuardNotOnPost(f"Охранник {self.full_name()} не на смене")
        self.on_duty = False
        return f"{self.full_name()} — смена завершена"

    def check_access(self, person):
        if not self.on_duty:
            raise SecurityGuardNotOnPost("Охранник не на посту!")
        return True