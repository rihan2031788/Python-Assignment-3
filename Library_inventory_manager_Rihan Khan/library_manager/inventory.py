import json
from pathlib import Path
from typing import List, Optional
from .book import Book
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, json_file_path: str = "data/books.json"):
        self.catalog: List[Book] = []
        self.file_path = Path(json_file_path)
        self.file_path.parent.mkdir(exist_ok=True)
        self.load_from_file()

    def add_book(self, book: Book):
        for existing in self.catalog:
            if existing.isbn == book.isbn:
                logger.error(f"Duplicate ISBN: {book.isbn} already exists!")
                return False

        self.catalog.append(book)
        self.save_to_file()
        logger.info(f"Added new book: {book.title} | {book.isbn}")
        return True

    def search_by_title(self, title_query: str) -> List[Book]:
        matches = [b for b in self.catalog if title_query.lower() in b.title.lower()]
        logger.info(f"Found {len(matches)} books for title query: `{title_query}`")
        return matches

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self.catalog:
            if book.isbn == isbn:
                logger.info(f"Located book with ISBN: {isbn}")
                return book
        logger.warning(f"No book found with ISBN: {isbn}")
        return None

    def display_all(self) -> List[Book]:
        logger.info(f"Displaying {len(self.catalog)} total books")
        return self.catalog

    def save_to_file(self):
        try:
            catalog_data = [book.to_dict() for book in self.catalog]
            with open(self.file_path, 'w') as catalog_file:
                json.dump(catalog_data, catalog_file, indent=4)
            logger.info(f"Successfully saved catalog to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save catalog: {str(e)}", exc_info=True)
            raise

    def load_from_file(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r') as catalog_file:
                    catalog_data = json.load(catalog_file)
                self.catalog = [Book(**book_data) for book_data in catalog_data]
                logger.info(f"Loaded {len(self.catalog)} books from {self.file_path}")
            else:
                self.save_to_file()
                logger.info(f"Created new catalog file at {self.file_path}")
        except json.JSONDecodeError:
            logger.error(f"Catalog file {self.file_path} is corrupted! Starting fresh.")
            self.catalog = []
            self.save_to_file()
        except Exception as e:
            logger.error(f"Failed to load catalog: {str(e)}", exc_info=True)
            raise