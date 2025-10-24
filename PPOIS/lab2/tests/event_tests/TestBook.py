import unittest
from events.book import Book
from people.student import Student
from academics.group import Group
from academics.major import Major
from academics.academy_level import AcademyLevel
class TestBook(unittest.TestCase):
    def setUp(self):

        major = Major("Компьютерные науки", "CS")
        level = AcademyLevel(1)
        group = Group("101", major, level, faculty=None, leader=None)
        self.student = Student(
            first_name="Иван",
            last_name="Иванов",
            email="ivanov@uni.ru",
            student_id="S001",
            group=group
        )

        self.book = Book(title="Python для всех", author="Гвидо ван Россум", isbn="1234567890")

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Python для всех")
        self.assertEqual(self.book.author, "Гвидо ван Россум")
        self.assertEqual(self.book.isbn, "1234567890")
        self.assertFalse(self.book.is_checked_out)
        self.assertIsNone(self.book.borrower)

    def test_check_out_book(self):
        self.book.check_out(self.student)
        self.assertTrue(self.book.is_checked_out)
        self.assertEqual(self.book.borrower, self.student)

    def test_check_out_already_checked_out_book_raises(self):
        self.book.check_out(self.student)
        with self.assertRaises(Exception) as context:
            self.book.check_out(self.student)
        self.assertIn("уже выдана", str(context.exception))

    def test_return_book(self):
        self.book.check_out(self.student)
        self.book.return_book()
        self.assertFalse(self.book.is_checked_out)
        self.assertIsNone(self.book.borrower)

    def test_return_not_checked_out_book_raises(self):
        with self.assertRaises(Exception) as context:
            self.book.return_book()
        self.assertIn("не выдана", str(context.exception))

if __name__ == "__main__":
    unittest.main()
