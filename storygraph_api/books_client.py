from storygraph_api.parse.books_parser import BooksParser
from storygraph_api.exception_handler import handle_exceptions
import json
from typing import Dict

class Book:
    @handle_exceptions
    def book_info(self, book_id: str) -> str:
        data = BooksParser.book_page(book_id)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def reading_progress(self, book_id: str, cookies: Dict[str, str]) -> str:
        progress = BooksParser.reading_progress(book_id, cookies)
        data = {"progress": progress}
        return json.dumps(data, indent=4)

    @handle_exceptions
    def get_read_dates(self, book_id: str, cookies: Dict[str, str]) -> str:
        data = BooksParser.get_read_dates(book_id, cookies)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def get_ai_summary(self, book_id: str, user_id: str) -> str:
        data = BooksParser.get_ai_summary(book_id, user_id)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def get_journal_entries(self, book_id: str, cookies: Dict[str, str]) -> str:
        data = BooksParser.journal_entries(book_id, cookies)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def search(self, query: str) -> str:
        data = BooksParser.search(query)
        return json.dumps(data, indent=4)
