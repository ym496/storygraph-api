import requests
from typing import Dict

class UserScraper:
    @staticmethod
    def get_profile_page(username: str) -> bytes:
        url = f"https://app.thestorygraph.com/profile/{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    @staticmethod
    def fetch_paginated_url(url: str, cookies: dict) -> bytes:
        headers = {
            'User-agent': 'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/91.0.4472.124 safari/537.36'
        }
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        return response.content

    @staticmethod
    def currently_reading(uname: str, cookies: Dict[str, str], page: int) -> bytes:
        url = f"https://app.thestorygraph.com/currently-reading/{uname}?page={page}"
        return UserScraper.fetch_paginated_url(url, cookies)

    @staticmethod
    def to_read(uname: str, cookies: Dict[str, str], page: int) -> bytes:
        url = f"https://app.thestorygraph.com/to-read/{uname}?page={page}"
        return UserScraper.fetch_paginated_url(url, cookies)

    @staticmethod
    def books_read(uname: str, cookies: Dict[str, str], page: int) -> bytes:
        url = f"https://app.thestorygraph.com/books-read/{uname}?page={page}"
        return UserScraper.fetch_paginated_url(url, cookies)

    @staticmethod
    def all_journal_entries(cookies: Dict[str, str], page: int) -> bytes:
        url = f"https://app.thestorygraph.com/journal?page={page}"
        return UserScraper.fetch_paginated_url(url, cookies)
