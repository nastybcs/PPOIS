class Location:
    def __init__(self,campus,building,room):
        self.campus = campus
        self.building = building
        self.room = room 

    def get_capacity(self):
        return self.room.capacity
        
    def is_over_capacity(self, expected_students):
        return expected_students>self.get_capacity()