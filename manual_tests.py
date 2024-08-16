"""
Basic Manual Testing of Components.
"""
import os
from dotenv import load_dotenv
# from storygraph_api.request.books_request import BooksScraper
# from storygraph_api.parse.books_parser import BooksParser
# from storygraph_api.request.user_request import UserScraper
# from storygraph_api.parse.user_parser import UserParser
# from storygraph_api.users_client import User
load_dotenv()

id = "a5da6127-beb2-44b9-aba6-f63de432777"
query = "pride and prejudice"
# testing book page info
# print(BooksScraper.main(id))
# print(BooksParser.book_page(id))

id = "fbdd6b7c-f512-47f2-aa94-d8bf0d5f5175"
from storygraph_api import Book
book = Book()
print(book.book_info(id))
# print(book.search(query))

# cookie = os.getenv('COOKIE')
# # print(UserScraper.currently_reading(uname,session_cookie=cookie))
# # print(UserParser.books_read(uname,cookie=cookie))
# user = User()
# print(user.books_read(uname,cookie=cookie))

#
# from storygraph_api.users_client import User
# from dotenv import load_dotenv
# load_dotenv()
# cookie = os.getenv('COOKIE')
# uname = 'clyrmze'
# user = User()
# result = user.books_read(uname,cookie=cookie)
# print(result)
