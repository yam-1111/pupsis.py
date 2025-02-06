from pupsis.api import APIRequester
from pupsis.scrapers import grades, schedule
from pupsis.utils.logs import Logger
from typing import Optional
import logging


class PUPSIS:
    def __init__(
        self,
        student_number: str,
        student_birthdate: str,
        password: str,
        # utility stuff
        headers: Optional[dict] = None,
        screenshot: Optional[bool] = False,
        logfile: Optional[str] = None,
        loglevel: Optional[str] = None,
    ):
        # password and student number
        self.student_number = student_number
        self.student_birthdate = student_birthdate
        self.password = password

        # logging utility stuff
        self.logfile = logfile
        self.loglevel = loglevel

        self.logger = Logger("pupSIS", log_file=self.logfile, level=self.loglevel)

    def grades(self):
        self.logger.debug(f"Fetching grades PUPSIS Credentials : {self.student_number} | {self.student_birthdate} | {self.password}")
        api = APIRequester(
            student_number=self.student_number,
            student_birthdate=self.student_birthdate,
            password=self.password,
            logfile=self.logfile,
            loglevel=self.loglevel,
        )
        return grades.Grade(api.get_grades())

    def schedule(self):
        api = APIRequester(
            student_number=self.student_number,
            student_birthdate=self.student_birthdate,
            password=self.password,
            logfile=self.logfile,
            loglevel=self.loglevel,
        )
        return schedule.Schedule(api.get_schedule())
