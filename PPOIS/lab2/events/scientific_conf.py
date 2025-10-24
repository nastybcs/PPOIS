class ScientificConference:  

    def __init__(self, title, date, location):
        self.title = title
        self.date = date
        self.location = location
        self.participants = []  
        self.presentations = []  

    def add_participant(self, person):
        if person not in self.participants:
            self.participants.append(person)

    def add_presentation(self, publication):
        if publication not in self.presentations:
            self.presentations.append(publication)

    def list_presentations(self):
        return [p.title for p in self.presentations]

    def list_participants(self):
        return [f"{p.first_name} {p.last_name}" for p in self.participants]