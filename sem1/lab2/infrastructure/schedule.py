from infrastructure.capacity_calculator import CapacityCalculator
from infrastructure.conflict_checker import ConflictChecker
from exceptions.errors import * 
class Schedule:
    def __init__(self):
        self.entries = []
        
    def check_room_capacity(self, location, activity_type, groups=None, subgroup=None):
        expected_students = CapacityCalculator.calculate(activity_type, groups,subgroup)
        if location.is_over_capacity(expected_students):
            raise CapacityError (f"Аудитория {location.room.room_number} вмещает" 
               f"{location.get_capacity()} Ожидаемое Количество:{expected_students}"
            )
        
        
    def is_location_conflicted(self, location, date_time, duration):
       if ConflictChecker.is_conflicted(self.entries, location,date_time, duration):
           raise LocationConflictedError(f"Аудитория {location.room.room_number} уже занята в это время")
            
        

    def add_entry(self, name,activity_type, date_time, duration, location, teacher,course,groups=None, subgroup=None):
        self.check_room_capacity(location, activity_type, groups, subgroup)
        self.is_location_conflicted(location, date_time, duration)
            
        entry = {
            "name": name,
            "date_time" : date_time,
            "duration" : duration,
            "location" : location,
            "teacher" : teacher,
            "groups" : groups or [],
            "subgroup" : subgroup,
            "activity_type" : activity_type.value,
            "course" : course,
        }
        self.entries.append(entry)