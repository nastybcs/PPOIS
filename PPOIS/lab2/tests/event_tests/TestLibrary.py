import unittest
from events.book import Book
from people.student import Student
from academics.group import Group
from academics.major import Major
from academics.academy_level import AcademyLevel
from events.library import Library

class TestLibrary(unittest.TestCase):
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

        self.library = Library("Главная библиотека")
        self.book1 = Book("Python для всех", "Гвидо ван Россум", "1234567890")
        self.book2 = Book("Алгоритмы", "Кормен", "0987654321")
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

    def test_add_and_list_books(self):
        self.assertIn(self.book1, self.library.books)
        self.assertIn(self.book2, self.library.books)
        self.assertEqual(len(self.library.books), 2)

    def test_remove_book(self):
        self.library.remove_book(self.book2)
        self.assertNotIn(self.book2, self.library.books)

    def test_remove_checked_out_book_raises(self):
        self.book1.check_out(self.student)
        with self.assertRaises(Exception) as context:
            self.library.remove_book(self.book1)
        self.assertIn("Нельзя удалить книгу", str(context.exception))

    def test_remove_nonexistent_book_raises(self):
        book3 = Book("Новая книга", "Автор", "1111111111")
        with self.assertRaises(Exception) as context:
            self.library.remove_book(book3)
        self.assertIn("не найдена", str(context.exception))

    def test_find_books_by_title(self):
        result = self.library.find_books_by_title("python")
        self.assertIn(self.book1, result)
        self.assertNotIn(self.book2, result)

    def test_find_books_by_author(self):
        result = self.library.find_books_by_author("кормен")
        self.assertIn(self.book2, result)
        self.assertNotIn(self.book1, result)

    def test_list_available_books(self):
        self.book1.check_out(self.student)
        available = self.library.list_available_books()
        self.assertIn(self.book2, available)
        self.assertNotIn(self.book1, available)

