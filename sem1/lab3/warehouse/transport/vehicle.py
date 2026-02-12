class Vehicle:
    def __init__(self, number, model, vehicle_type, capacity_kg):
        self.number = number
        self.model = model
        self.type = vehicle_type
        self.capacity_kg = capacity_kg or vehicle_type.capacity()
        self.driver = None
        self.current_load = 0
        self.is_available = True

    def assign_driver(self, driver):
        if self.driver:
            raise ValueError(f"Машина {self.number} уже закреплена за {self.driver.full_name()}")
        self.driver = driver
        driver.vehicle = self
        return f"Водитель {driver.full_name()} закреплён за {self}"

    def load_order(self, order):
        weight = sum(
            (getattr(item.product, 'weight', 0) or 0) * item.quantity
            for item in order.items
        )
        if self.current_load + weight > self.capacity_kg:
            raise ValueError(
                f"Превышена грузоподъёмность: {self.current_load + weight} > {self.capacity_kg} кг"
            )
        self.current_load += weight

    def unload(self):
        self.current_load = 0

    def __str__(self):
        return (f"{self.type.name_ru} {self.model} ({self.number}), "
                f"вместимость: {self.capacity_kg} кг")