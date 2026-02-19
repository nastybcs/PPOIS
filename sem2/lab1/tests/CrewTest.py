import unittest
from objects.CrewMember import CrewMember
from objects.Crew import Crew


class TestCrewUncoveredLines(unittest.TestCase):

    def setUp(self):
        self.crew = Crew()
        self.member = CrewMember("Тест") 

    def test_board_method(self):
        self.assertFalse(self.crew._Crew__is_ready)
        result = self.crew.board()
        self.assertTrue(self.crew.is_ready)
        self.assertTrue(result)


    def test_str_empty_crew(self):
        crew_str = str(self.crew)
        self.assertIn("Crew: empty", crew_str)

    def test_str_with_members(self):
        self.crew.add_member(self.member)
        crew_str = str(self.crew)
        self.assertIn("Crew (1 people, not ready):", crew_str)
        self.assertIn("    Тест", crew_str)  

    def test_str_with_ready_status(self):
        self.crew.add_member(self.member)
        self.crew.board()  

        crew_str = str(self.crew)
        self.assertIn("ready", crew_str)

    def test_init_creates_empty_members_list(self):
        crew = Crew()
        self.assertTrue(hasattr(crew, "_Crew__members"))
        self.assertEqual(len(crew._Crew__members), 0)
        self.assertIsInstance(crew._Crew__members, list)

    def test_init_sets_is_ready_false(self):
        crew = Crew()
        self.assertTrue(hasattr(crew, "_Crew__is_ready"))
        self.assertFalse(crew._Crew__is_ready)

    def test_is_ready_property_returns_correct_value(self):
        crew = Crew()
        self.assertFalse(crew.is_ready)
        crew._Crew__is_ready = True
        self.assertTrue(crew.is_ready)

        crew._Crew__is_ready = False
        self.assertFalse(crew.is_ready)

    def test_is_ready_property_read_only(self):
        crew = Crew()
        with self.assertRaises(AttributeError):
            crew.is_ready = True
            
    def test_from_dict_with_valid_data(self):
        data = {
            "members": [
                {"name": "Иван"},
                {"name": "Петр"}
            ],
            "is_ready": True
        }
        
        self.crew.from_dict(data)
        members = self.crew._Crew__members
        self.assertEqual(len(members), 2)
        self.assertEqual(members[0].name, "Иван")
        self.assertEqual(members[1].name, "Петр")
        self.assertTrue(self.crew._Crew__is_ready)
    
    def test_from_dict_with_role_ignored(self):
        data = {
            "members": [
                {"name": "Иван", "role": "мехвод"},  
            ],
            "is_ready": False
        }
        
        self.crew.from_dict(data)
        
        members = self.crew._Crew__members
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0].name, "Иван")
