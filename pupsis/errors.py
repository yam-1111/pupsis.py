
class LoginError(Exception):
    """Exception raised for incorrect login credentials.

    Attributes:
        message: Explanation of the error.
        kwargs: Dictionary containing the credentials used in the login attempt.
    """

    def __init__(self, message: str, **kwargs):
        self.message = message
        self.kwargs = kwargs
        super().__init__(self.message)

    def __str__(self):
        # Format credentials as key-value pairs on new lines
        credentials = "\n".join(f"{key}: {value}" for key, value in self.kwargs.items())
        return f"{self.message}\n------\nCredentials:\n{credentials}"

    

class MultipleLoginAttempt(Exception):
    """Exception raised when the user has exceeded the maximum login attempts.
    """
    def __init__(self):
        self.message = "Maximum log in attempts exceeded. Please log in again after 60min/s."
        super().__init__(self.message)

class SurveyError(Exception):
    """Exception raised when the user has not completed the survey.
    """
    def __init__(self):
        self.message = "Please complete the survey first."
        super().__init__(self.message)
