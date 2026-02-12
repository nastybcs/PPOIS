from datetime import datetime
class RoutePoint:
    def __init__(self, address, description=None):
        self.address = address  
        self.description = description or "Промежуточная точка"
        self.visited = False
        self.arrival_time = None

    def mark_visited(self):
        self.visited = True
        self.arrival_time = datetime.now()