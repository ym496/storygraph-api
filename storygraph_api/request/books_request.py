import requests
from storygraph_api.exception_handler import request_exception

class BooksScraper:
    @staticmethod
    @request_exception
    def fetch_url(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    @staticmethod
    def main(book_id):
        url = f"https://app.thestorygraph.com/books/{book_id}"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def community_reviews(book_id):
        url = f"https://app.thestorygraph.com/books/{book_id}/community_reviews"
        return BooksScraper.fetch_url(url)

    @staticmethod
    def search(query):
        formatted_query = query.replace(' ', '%20')
        url = f"https://app.thestorygraph.com/browse?search_term={formatted_query}"
        return BooksScraper.fetch_url(url)
