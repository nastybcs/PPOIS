from people.person import Person
from exceptions.errors import *
from events.event import Event
class EventSecretary(Person):
    def __init__(self, first_name, last_name, email, secretary_id, faculty):
        super().__init__(first_name, last_name, email)
        self.secretary_id = secretary_id
        self.faculty = faculty
        self.events = []

    def create_event(self, title, date_time, location, organiser, groups):
        event = Event(title, date_time, location, organiser, groups)
        self.events.append(event)
        return event

    def list_event(self):
        return [str(event.title) for event in self.events]

    def find_event_for_group(self, group):
        return [
            event for event in self.events
            if any(g.name == group.name for g in event.groups)
        ]

    def delete_event(self, event):
        if event not in self.events:
            raise EventNotFoundError(f"Мероприятие {event.title} не найдено")
        self.events.remove(event)

    def find_events_by_date(self,target_date):
        return [
            event for event in self.events
            if event.date_time.date()== target_date
        ]
