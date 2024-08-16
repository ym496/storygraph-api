from storygraph_api.parse.books_parser import BooksParser
from storygraph_api.exception_handler import handle_exceptions
import json

class Book:
    @handle_exceptions
    def book_info(self,book_id):
        data = BooksParser.book_page(book_id)
        return json.dumps(data,indent=4)

    @handle_exceptions
    def search(self,query):
        data = BooksParser.search(query)
        return json.dumps(data,indent=4)
