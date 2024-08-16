class StoryGraphAPIError(Exception):
    """Base class for exceptions in StoryGraphAPI"""
    pass
class RequestError(StoryGraphAPIError):
    """Exception raised for errors during the request."""

    def __init__(self, message="An error occurred during the request."):
        self.message = message
        super().__init__(self.message)

class ParsingError(StoryGraphAPIError):
    """Exception raised for errors during parsing responses."""

    def __init__(self, message="An error occurred while parsing the response."):
        self.message = message
        super().__init__(self.message)
class UnexpectedError(StoryGraphAPIError):
    """Exception raised for unexpected errors."""

    def __init__(self, message="An unexpected error occurred."):
        self.message = message
        super().__init__(self.message)
