from pupsis.api import APIRequester
from pupsis.scrapers import grades, schedule
from pupsis.utils.logs import Logger
from pupsis.utils.types import validate_student_number, validate_student_birthdate
from pupsis.errors import InvalidStudentNumber, InvalidBirthdate
from typing import Optional


class PUPSIS:
    """
    Class used for instatiating a PUPSIS object.

    Attributes:
        student_number (str): The student number of the user.
        student_birthdate (str): The birthdate of the user.
        password (str): The password of the user.
        headers (dict): The headers to be used in the request.
        logfile (str): The path to the log file.
        loglevel (str): The logging level.
        request_delay (int): The delay between requests.
    
    Example:
    >>> student = PUPSIS(student_number="2020-12345-MN-0", student_birthdate="1/02/2003", password="mypassword")
    Raises:
        InvalidStudentNumber: If the student number is invalid.
        InvalidBirthdate: If the birthdate
    """
    def __init__(
        self,
        student_number: str,
        student_birthdate: str,
        password: str,
        # utility stuff
        headers: Optional[dict] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Referer": "https://sis8.pup.edu.ph/student/",
            "Accept-Language": "en-US,en;q=0.9",
        },
        screenshot: Optional[bool] = False,
        logfile: Optional[str] = None,
        loglevel: Optional[str] = None,
        request_delay: Optional[int] = 2,
    ):
        # password and student number
        self.student_number = self.set_student_number(student_number)
        self.student_birthdate = self.set_student_birthdate(student_birthdate)
        self.password = password

        # headers
        self.headers = headers

        # logging utility stuff
        self.logfile = logfile
        self.loglevel = loglevel

        # implement delay
        self.request_delay = request_delay

        self.logger = Logger("pupSIS", log_file=self.logfile, level=self.loglevel)

    # validates the student number and student birthdate before making actual request to prevent server overload

    @staticmethod
    def set_student_number(student_number: str):
        """Validates the student number format."""
        try:
            return validate_student_number(student_number)
        except ValueError:
            raise InvalidStudentNumber(student_number)

    @staticmethod
    def set_student_birthdate(student_birthdate: str):
        """Validates the student birthdate format."""
        try:
            return validate_student_birthdate(student_birthdate)
        except ValueError:
            raise InvalidBirthdate(student_birthdate)

    # api methods
    def grades(self):
        """
        Fetches the student grades from the PUPSIS portal

        initializes an `APIRequester` instance using the student's credentials and retrieves the grades data.

        Returns:
            Grade: An instance of the `Grade` class containing the parsed grades data.
                latest() - returns the latest semester grades
                all() - returns all semester grades from the start to the latest in descending order
        Example:
        >>> student = PUPSIS(student_number="2020-12345-MN-0", student_birthdate="1/02/2003", password="mypassword")    
        >>> grades = student.grades()
        >>> latest_grades = grades.latest()
        >>> print(latest_grades) # returns grades properties

        Raises:
            SurveyError: If the user has not completed the survey.
            LoginError: If the login credentials are incorrect.
            MultipleLoginAttempt: If the user has exceeded the maximum login attempts.clear
        """
        self.logger.debug(
            f"Fetching grades PUPSIS Credentials : {self.student_number} | {self.student_birthdate} | {self.password}"
        )
        api = APIRequester(
            student_number=self.student_number,
            student_birthdate=self.student_birthdate,
            password=self.password,
            logfile=self.logfile,
            loglevel=self.loglevel,
            headers=self.headers,
            request_delay=self.request_delay,

        )
        return grades.Grade(api.get_grades())

    def schedule(self):
        """
        Fetches the student schedule from the PUPSIS portal

        initializes an `APIRequester` instance using the student's credentials 
        and retrieves the schedule data. The response is then processed into a `Schedule` object.

        Returns:
            Schedule: An instance of the `Schedule` class containing the parsed schedule data.

        Example:
        >>> student = PUPSIS(student_number="2020-12345-MN-0", student_birthdate="1/02/2003", password="mypassword")
        >>> schedule = student.schedule()
        >>> print(schedule)

        Raises:
            SurveyError: If the user has not completed the survey.
            LoginError: If the login credentials are incorrect.
            MultipleLoginAttempt: If the user has exceeded the maximum login attempts.

        """
        api = APIRequester(
            student_number=self.student_number,
            student_birthdate=self.student_birthdate,
            password=self.password,
            logfile=self.logfile,
            loglevel=self.loglevel,
            headers=self.headers,
            request_delay=self.request_delay,
        )
        return schedule.Schedule(api.get_schedule())
