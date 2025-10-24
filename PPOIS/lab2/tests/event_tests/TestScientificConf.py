import unittest

from people.person import Person 
from events.publication import Publication
from events.publication_type import PublicationType
from events.scientific_conf import ScientificConference

class TestScientificConference(unittest.TestCase):
    def setUp(self):

        self.participant1 = Person("Иван", "Иванов", "ivan@uni.ru")
        self.participant2 = Person("Мария", "Петрова", "maria@uni.ru")

    
        self.pub1 = Publication(
            title="Методы AI",
            authors=[self.participant1],
            pub_type=PublicationType.JOURNAL,
            date="2025-10-22",
            venue="Journal of AI"
        )
        self.pub2 = Publication(
            title="Нейронные сети",
            authors=[self.participant2],
            pub_type=PublicationType.CONFERENCE,
            date="2025-10-22",
            venue="Conf AI"
        )

 
        self.conference = ScientificConference(
            title="AI Conference 2025",
            date="2025-11-01",
            location="Москва"
        )

    def test_add_participants(self):
        self.conference.add_participant(self.participant1)
        self.conference.add_participant(self.participant2)
        self.assertIn(self.participant1, self.conference.participants)
        self.assertIn(self.participant2, self.conference.participants)

    def test_add_presentations(self):
        self.conference.add_presentation(self.pub1)
        self.conference.add_presentation(self.pub2)
        self.assertIn(self.pub1, self.conference.presentations)
        self.assertIn(self.pub2, self.conference.presentations)

    def test_list_participants(self):
        self.conference.add_participant(self.participant1)
        self.conference.add_participant(self.participant2)
        participants_list = self.conference.list_participants()
        self.assertIn("Иван Иванов", participants_list)
        self.assertIn("Мария Петрова", participants_list)

    def test_list_presentations(self):
        self.conference.add_presentation(self.pub1)
        self.conference.add_presentation(self.pub2)
        presentations_list = self.conference.list_presentations()
        self.assertIn("Методы AI", presentations_list)
        self.assertIn("Нейронные сети", presentations_list)


