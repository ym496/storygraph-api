from storygraph_api.parse.user_parser import UserParser
from storygraph_api.request.user_request import UserScraper
from storygraph_api.exception_handler import handle_exceptions
import json

class User:
    @handle_exceptions
    def get_user_id(self, username: str) -> str:
        data = UserParser.get_user_id(username)
        return json.dumps(data, indent=4)

    def _fetch_paginated_books(self, fetch_function, uname, cookies):
        all_books = []
        page = 1
        while True:
            content = fetch_function(uname, cookies, page)
            books = UserParser.parse_html(content)
            if not books:
                break
            all_books.extend(books)
            page += 1
        return all_books

    @handle_exceptions
    def currently_reading(self, uname, cookies):
        data = self._fetch_paginated_books(UserScraper.currently_reading, uname, cookies)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def to_read(self, uname, cookies):
        data = self._fetch_paginated_books(UserScraper.to_read, uname, cookies)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def books_read(self, uname, cookies):
        data = self._fetch_paginated_books(UserScraper.books_read, uname, cookies)
        return json.dumps(data, indent=4)

    @handle_exceptions
    def get_all_journal_entries(self, cookies):
        all_entries = []
        page = 1
        while True:
            content = UserScraper.all_journal_entries(cookies, page)
            entries = UserParser.all_journal_entries(content)
            if not entries:
                break
            all_entries.extend(entries)
            page += 1
        return json.dumps(all_entries, indent=4)