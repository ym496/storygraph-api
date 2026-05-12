from storygraph_api.request.user_request import UserScraper
from storygraph_api.exception_handler import parsing_exception
from bs4 import BeautifulSoup

class UserParser:
    @staticmethod
    @parsing_exception 
    def parse_html(html, id_enclosure=None):
        soup = BeautifulSoup(html, 'html.parser')
        if id_enclosure:
            soup = soup.find_all('div', attrs={"id": id_enclosure})[0]
        books_list = []
        books = soup.find_all('div', class_="book-title-author-and-series")
        for book in books:
            a_list = book.find_all('a')
            authors = []
            for a in a_list:
                if a['href'].startswith("/books/"):
                    title = a.text.strip()
                    book_id = a['href'].split('/')[-1]
                if a['href'].startswith("/authors/"):
                    authors.append(a.text.strip())
            books_list.append({
                'title': title,
                'book_id': book_id,
                'authors': authors
                })
        data = list({(book['title'], book['book_id']): book for book in books_list}.values())
        return data

    @staticmethod
    def currently_reading(uname, cookie):
        content = UserScraper.currently_reading(uname,cookie)
        return UserParser.parse_html(content)

    @staticmethod
    def to_read(uname, cookie):
        content = UserScraper.to_read(uname,cookie)
        return UserParser.parse_html(content)

    @staticmethod
    def up_next(uname, cookie):
        content = UserScraper.to_read(uname, cookie)
        return UserParser.parse_html(content, "up-next-section")

    @staticmethod
    def books_read(uname, cookie):
        content = UserScraper.books_read(uname,cookie)
        return UserParser.parse_html(content)
