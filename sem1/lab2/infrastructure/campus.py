from exceptions.errors import *
class Campus:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.buildings = []

    def add_building(self, build):
        if build not in self.buildings:
            self.buildings.append(build)

    def list_of_buildings(self):
        return [b.name for b in self.buildings]
        
    def remove_building(self, build_to_remove):
        if build_to_remove not in self.buildings:
            raise BuildingNotFoundError (f"Корпус номер {build_to_remove.name} не найдена в {self.name} корпусе ")
        self.buildings.remove(build_to_remove)