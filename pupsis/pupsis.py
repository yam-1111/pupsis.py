from typing import Optional
from pupsis.api import APIRequester
from pupsis.scrapers import grades, schedule
from pupsis.utils.logs import Logger
from pupsis.utils import get_stream_file
from pupsis.utils.types import *
from pupsis.errors import *


class PUPSIS:
    def __init__(
        self,
        student_number: Optional[str] = None,
        student_birthdate: Optional[str] = None,
        password: Optional[str] = None,
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

        self.student_number = student_number
        self.student_birthdate = student_birthdate
        self.password = password
        self.headers = headers
        self.logfile = logfile
        self.loglevel = loglevel
        self.logger = Logger("pupSIS", log_file=self.logfile, level=self.loglevel)
        self.request_delay = request_delay

        if self.request_delay <= 0:
            self.logger.warning(REQUEST_DELAY_ZERO)

        if self.student_number:
            self.student_number = self.set_student_number(self.student_number)

        if self.student_birthdate:
            self.student_birthdate = self.set_student_birthdate(self.student_birthdate)

        if not any([self.student_number, self.student_birthdate, self.password]):
            self.logger.info("PUPSIS instance created without credentials.")

    @staticmethod
    def set_student_number(student_number: str):
        try:
            return validate_student_number(student_number)
        except ValueError:
            raise InvalidStudentNumber(student_number)

    @staticmethod
    def set_student_birthdate(student_birthdate: str):
        try:
            return validate_student_birthdate(student_birthdate)
        except ValueError:
            raise InvalidBirthdate(student_birthdate)

    def grades(self, grades_filename: Optional[str] = None):
        """
        Fetches the student grades from the PUPSIS portal

        initializes an `APIRequester` instance using the student's credentials and retrieves the grades data.

        Attributes:
            grades_filename (str): The path to the grades file. 

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
            ValueError: If the required credentials are missing. (if filepath is not provided)
        """
        if grades_filename:
            self.logger.info(f"Fetching grades from file: {grades_filename}")
            return grades.Grade(get_stream_file(grades_filename))

        missing_fields = [
            field
            for field, value in {
                "student_number": self.student_number,
                "student_birthdate": self.student_birthdate,
                "password": self.password,
            }.items()
            if not value
        ]

        if missing_fields:
            raise ValueError(
                f"Missing required credentials for fetching grades: {', '.join(missing_fields)}"
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

    def schedule(self, schedule_filename: Optional[str] = None):
        """
        Fetches the student schedule from the PUPSIS portal

        initializes an `APIRequester` instance using the student's credentials 
        and retrieves the schedule data. The response is then processed into a `Schedule` object.

        Attributes:
            schedule_filename (str): The path to the schedule file.

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
            ValueError: If the required credentials are missing. (if filepath is not provided)

        """
        if schedule_filename:
            self.logger.info(f"Fetching schedule from file: {schedule_filename}")
            return schedule.Schedule(get_stream_file(schedule_filename))

        missing_fields = [
            field
            for field, value in {
                "student_number": self.student_number,
                "student_birthdate": self.student_birthdate,
                "password": self.password,
            }.items()
            if not value
        ]

        if missing_fields:
            raise ValueError(
                f"Missing required credentials for fetching schedule: {', '.join(missing_fields)}"
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
        return schedule.Schedule(api.get_schedule())
