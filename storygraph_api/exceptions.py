class StoryGraphAPIError(Exception):
    pass
class RequestError(StoryGraphAPIError):

    def __init__(self, message="An error occurred during the request."):
        self.message = message
        super().__init__(self.message)

class ParsingError(StoryGraphAPIError):

    def __init__(self, message="An error occurred while parsing the response."):
        self.message = message
        super().__init__(self.message)
class UnexpectedError(StoryGraphAPIError):

    def __init__(self, message="An unexpected error occurred."):
        self.message = message
        super().__init__(self.message)
