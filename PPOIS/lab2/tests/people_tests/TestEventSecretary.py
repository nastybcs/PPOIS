import unittest
from datetime import datetime
from events.event import Event
from exceptions.errors import EventNotFoundError
from people.event_secretary import EventSecretary

class TestEventSecretary(unittest.TestCase):
    def setUp(self):
        self.faculty = "Факультет информатики"
        self.secretary = EventSecretary("Елена", "Иванова", "elena@example.com", "SEC002", self.faculty)
        self.date_time = datetime(2025, 10, 22, 10, 0) 
        self.group = type('Group', (), {'name': 'Group A'})()  
        self.event = Event("Лекция", self.date_time, "Ауд. 101", "Преподаватель", [self.group])

    def test_initialization(self):
        self.assertEqual(self.secretary.first_name, "Елена")
        self.assertEqual(self.secretary.last_name, "Иванова")
        self.assertEqual(self.secretary.email, "elena@example.com")
        self.assertEqual(self.secretary.secretary_id, "SEC002")
        self.assertEqual(self.secretary.faculty, self.faculty)
        self.assertEqual(len(self.secretary.events), 0)

    def test_create_event(self):
        event = self.secretary.create_event("Семинар", self.date_time, "Ауд. 102", "Оргкомитет", [self.group])
        self.assertEqual(len(self.secretary.events), 1)
        self.assertEqual(event.title, "Семинар")
        self.assertIn(event, self.secretary.events)

    def test_list_event(self):
        self.secretary.create_event("Семинар", self.date_time, "Ауд. 102", "Оргкомитет", [self.group])
        event_list = self.secretary.list_event()
        self.assertEqual(len(event_list), 1)
        self.assertIn("Семинар", event_list)

    def test_find_event_for_group(self):
        self.secretary.create_event("Семинар", self.date_time, "Ауд. 102", "Оргкомитет", [self.group])
        events = self.secretary.find_event_for_group(self.group)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Семинар")

    def test_delete_event_success(self):
        event = self.secretary.create_event("Семинар", self.date_time, "Ауд. 102", "Оргкомитет", [self.group])
        self.secretary.delete_event(event)
        self.assertEqual(len(self.secretary.events), 0)

    def test_delete_event_not_found(self):
        event = Event("Несуществующее событие", self.date_time, "Ауд. 103", "Оргкомитет", [self.group])
        with self.assertRaises(EventNotFoundError):
            self.secretary.delete_event(event)

    def test_find_events_by_date(self):
        self.secretary.create_event("Семинар", self.date_time, "Ауд. 102", "Оргкомитет", [self.group])
        another_date = datetime(2025, 10, 23, 10, 0)
        self.secretary.create_event("Лекция", another_date, "Ауд. 101", "Преподаватель", [self.group])
        events = self.secretary.find_events_by_date(self.date_time.date())
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Семинар")

    def tearDown(self):
        self.secretary.events.clear()

