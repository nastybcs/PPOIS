class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False
        self.borrower = None

    def check_out(self, student):
        if self.is_checked_out:
            raise Exception(f"Книга '{self.title}' уже выдана {self.borrower.first_name} {self.borrower.last_name}")
        self.is_checked_out = True
        self.borrower = student

    def return_book(self):
        if not self.is_checked_out:
            raise Exception(f"Книга '{self.title}' не выдана")
        self.is_checked_out = False
        self.borrower = None