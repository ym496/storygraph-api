import json
import requests
from functools import wraps
from storygraph_api.exceptions import RequestError, ParsingError, UnexpectedError
from selenium.common.exceptions import WebDriverException

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (RequestError, ParsingError) as e:
            return json.dumps({"error": e.message}, indent=4)
        except Exception as e:
            unexpected_error = UnexpectedError(f"An unexpected error occurred: {str(e)}")
            return json.dumps({"error": unexpected_error.message}, indent=4)
    return wrapper

def request_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            raise RequestError(f"A network error occurred: {str(e)}") from e
        except WebDriverException as e:
            raise RequestError(f"A browser automation error occurred: {str(e)}") from e
    return wrapper

def parsing_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AttributeError, IndexError, TypeError, ValueError) as e:
            raise ParsingError(f"Failed to parse page content. The website structure may have changed. Details: {str(e)}") from e
    return wrapper
