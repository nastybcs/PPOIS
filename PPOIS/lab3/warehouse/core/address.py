class Address:
    def __init__(self,city, street, house_num ):
        self.city = city
        self.street = street
        self.house_num = house_num

    def full_address(self):
        return f"{self.city}, {self.street}, {self.house_num}"
    def short_address(self):
        return f"{self.street}, {self.house_num}"
