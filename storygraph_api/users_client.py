from storygraph_api.parse.user_parser import UserParser
from storygraph_api.exception_handler import handle_exceptions
import json

class User:
    @handle_exceptions
    def currently_reading(self,uname,cookie):
        data = UserParser.currently_reading(uname,cookie)
        return json.dumps(data,indent=4)

    @handle_exceptions
    def to_read(self,uname,cookie):
        data = UserParser.to_read(uname,cookie)
        return json.dumps(data,indent=4)

    @handle_exceptions
    def books_read(self,uname,cookie):
        data = UserParser.books_read(uname,cookie)
        return json.dumps(data,indent=4)
