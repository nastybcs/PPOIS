from exceptions.errors import *
class Building:
    def __init__(self,name,building_code, campus):
        self.name = name
        self.building_code = building_code
        self.campus = campus
        self.rooms = []

    def add_room(self,room):
       if room not in self.rooms:
           self.rooms.append(room)
        
    def list_of_rooms(self):
        return [r.room_number for r in self.rooms]
        
    def remove_room(self,room_to_remove):
        if room_to_remove not in self.rooms:
            raise RoomNotFoundError (f"Аудитория номер {room_to_remove.room_number} не найдена в {self.building_code} корпусе ")
        self.rooms.remove(room_to_remove)