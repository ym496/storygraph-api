import requests
from typing import Dict

class BooksScraper:
    @staticmethod
    def fetch_url(url: str, cookies: Dict[str, str] | None = None, params: Dict[str, str] | None = None) -> bytes:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, cookies=cookies, headers=headers, params=params)
        response.raise_for_status()
        return response.content

    @staticmethod
    def post_url(url: str, cookies: Dict[str, str] | None = None, data: Dict[str, str] | None = None) -> bytes:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, cookies=cookies, headers=headers, data=data)
        response.raise_for_status()
        return response.content

    @staticmethod
    def main(book_id: str) -> bytes:
        url = f"https://app.thestorygraph.com/books/{book_id}"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def book_page_authenticated(book_id: str, cookies: Dict[str, str]) -> bytes:
        url = f"https://app.thestorygraph.com/books/{book_id}"
        return BooksScraper.fetch_url(url, cookies=cookies)

    @staticmethod
    def community_reviews(book_id: str) -> bytes:
        url = f"https://app.thestorygraph.com/books/{book_id}/community_reviews"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def content_warnings(book_id: str) -> bytes:
        url = f"https://app.thestorygraph.com/books/{book_id}/content_warnings"
        return BooksScraper.fetch_url(url)
    
    @staticmethod
    def get_read_dates_form(book_id: str, read_instance_id: str, cookies: Dict[str, str]) -> bytes:
        url = f"https://app.thestorygraph.com/edit-read-instance-from-book?book_id={book_id}&read_instance_id={read_instance_id}"
        return BooksScraper.post_url(url, cookies=cookies)

    @staticmethod
    def get_journal_entry_form(book_id: str, journal_entry_id: str, cookies: Dict[str, str]) -> bytes:
        url = f"https://app.thestorygraph.com/edit-journal-entry-from-book?book_id={book_id}&journal_entry_id={journal_entry_id}"
        return BooksScraper.post_url(url, cookies=cookies)

    @staticmethod
    def get_ai_summary(book_id: str, user_id: str) -> bytes:
        url = f"https://app.thestorygraph.com/personalized-preview.turbo_stream"
        params = {'book_id': book_id, 'personalized': 'false', 'user_id': user_id}
        return BooksScraper.fetch_url(url, params=params)

    @staticmethod
    def get_journal_page(book_id: str, cookies: Dict[str, str]) -> bytes:
        url = "https://app.thestorygraph.com/journal"
        params = {'book_id': book_id}
        return BooksScraper.fetch_url(url, cookies=cookies, params=params)

    @staticmethod
    def search(query: str) -> bytes:
        url = "https://app.thestorygraph.com/browse"
        params = {'search_term': query}
        return BooksScraper.fetch_url(url, params=params)