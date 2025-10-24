class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            if book.is_checked_out:
                raise Exception(f"Нельзя удалить книгу '{book.title}', она выдана {book.borrower.first_name} {book.borrower.last_name}")
            self.books.remove(book)
        else:
            raise Exception(f"Книга '{book.title}' не найдена в библиотеке '{self.name}'")

    def find_books_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def find_books_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]

    def list_available_books(self):
        return [book for book in self.books if not book.is_checked_out]

    def list_all_books(self):
        return self.books