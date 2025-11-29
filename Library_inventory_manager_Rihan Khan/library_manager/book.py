class Book:
    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        if status not in ["available", "issued"]:
            raise ValueError("Status must be 'available' or 'issued'")
        self.status = status

    def __str__(self):
        return f"\"{self.title}\" by {self.author} | ISBN: {self.isbn} | Status: {self.status.upper()}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"