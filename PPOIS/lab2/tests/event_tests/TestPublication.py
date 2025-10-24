import unittest
from people.person import Person 
from events.publication import Publication
from events.publication_type import PublicationType

class TestPublication(unittest.TestCase):
    def setUp(self):
        # Создаем авторов
        self.author1 = Person("Иван", "Иванов", "ivan@uni.ru")
        self.author2 = Person("Мария", "Петрова", "maria@uni.ru")

        # Создаем публикацию
        self.publication = Publication(
            title="Новые методы AI",
            authors=[self.author1, self.author2],
            pub_type=PublicationType.JOURNAL,
            date="2025-10-22",
            venue="Journal of AI Research",
            doi="10.1234/jair.5678"
        )

    def test_publication_creation(self):
        self.assertEqual(self.publication.title, "Новые методы AI")
        self.assertEqual(self.publication.pub_type, PublicationType.JOURNAL)
        self.assertEqual(self.publication.venue, "Journal of AI Research")
        self.assertEqual(self.publication.doi, "10.1234/jair.5678")
        self.assertIn(self.author1, self.publication.authors)
        self.assertIn(self.author2, self.publication.authors)

    def test_authors_receive_publication(self):
        self.assertIn(self.publication, self.author1.publications)
        self.assertIn(self.publication, self.author2.publications)

    def test_list_authors(self):
        authors_list = self.publication.list_authors()
        self.assertIn("Иван Иванов", authors_list)
        self.assertIn("Мария Петрова", authors_list)

if __name__ == "__main__":
    unittest.main()
