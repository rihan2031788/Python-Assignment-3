import pytest
from pathlib import Path
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

def test_book_creation():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.is_available() is True
    assert str(book) == "\"Test Book\" by Test Author | ISBN: 1234567890 | Status: AVAILABLE"

def test_book_issue_return():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.issue() is True
    assert book.is_available() is False
    assert book.issue() is False
    assert book.return_book() is True
    assert book.is_available() is True
    assert book.return_book() is False

def test_inventory_add_duplicate_isbn(tmp_path):
    test_file = tmp_path / "test.json"
    inv = LibraryInventory(json_file_path=str(test_file))
    book1 = Book("Test 1", "Auth", "0000")
    book2 = Book("Test 2", "Auth2", "0000")

    assert inv.add_book(book1) is True
    assert inv.add_book(book2) is False
    assert len(inv.display_all()) == 1

def test_inventory_search(tmp_path):
    test_file = tmp_path / "test.json"
    inv = LibraryInventory(json_file_path=str(test_file))
    inv.add_book(Book("Python Basics", "A. Codemaker", "1111"))
    inv.add_book(Book("Advanced Python", "B. Codemaker", "2222"))

    title_results = inv.search_by_title("python")
    assert len(title_results) == 2
    isbn_result = inv.search_by_isbn("1111")
    assert isbn_result is not None
    assert isbn_result.title == "Python Basics"