from tls_client import Session
from pupsis.utils.logs import Logger
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Optional, Required
import logging

from pupsis.scraper.grades import Grade


class pupSIS:
    def __init__(
        self,
        student_number: str,
        student_birthdate: str,
        password: str,
        # utility stuff
        headers: Optional[dict] = None,
        screenshot : Optional[bool] = False,
        logfile : Optional[str] = None,
        loglevel :  Optional[str] = logging.INFO,
    ):
        self.student_number = student_number
        self.student_birthdate = student_birthdate.split("/")
        self.password = password

        # Set default headers if none are provided
        self.headers = headers or {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "cache-control": "max-age=0",
            "referer": "https://sis8.pup.edu.ph/student/",
            "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }
        self.screenshot = screenshot

        # birthdate
        self.birthdate_month = self.student_birthdate[0]
        self.birthdate_day = self.student_birthdate[1]
        self.birthdate_year = self.student_birthdate[2]

        # utilities
        self.init_url = "https://sis8.pup.edu.ph/student/"
        self.logger = Logger("pupSIS", log_file=logfile, level=loglevel)
        self.session = Session(
            client_identifier="chrome126",
            random_tls_extension_order=True,
        )

    @property
    def csrf_token(self):
        """
        extracts the csrf to be able to login on the SIS
        """
        self.logger.info("Extracting CSRF token")
        csrf = []

        csrf_request = self.session.get(self.init_url, headers=self.headers)
        tree = LexborHTMLParser(csrf_request.text)

        for x in ["input[name='csrf_token']", "input#tempcsrf"]:
            _csrf = tree.css_first(x).attrs["value"]
            csrf.append(_csrf)

        self.logger.debug(f"CSRF token extracted : {csrf}")
        return tuple(csrf)

    def login(self):
        """
        logs in the student to the SIS
        """
        self.logger.info("Logging in to SIS")

        csrf = self.csrf_token
        payload = [
            ("csrf_token", csrf[0]),
            ("csrf_token", csrf[1]),
            ("studno", self.student_number),
            ("SelectMonth", 8),
            ("SelectDay", 20),
            ("SelectYear", 2004),
            ("password", self.password),
            ("Login", "Sign in"),
        ]

        login_request = self.session.post(
            self.init_url,
            headers=self.headers,
            data=payload,
        )
        if login_request.status_code == 200:
            self.logger.info("Logged in successfully")
        else:
            self.logger.error(f"Failed to login {login_request.status_code}")

    # pupSIS methods


    def grades(self):
        """
        Fetches the grades from the SIS (Student Information System).

        Returns:
            Grade: An object containing methods and attributes to access grades.

            Methods:
                latest() -> dict: Returns the latest academic semester grades.

                all() -> list: Returns all grades from the latest to the first academic semester.

                get(semester: int) -> dict: Returns the grades for the specified academic semester.
        """
        self.login()
        grades_url = self.init_url + "grades"
        grades_request = self.session.get(grades_url, headers=self.headers)

        if grades_request.status_code == 200:
            return Grade(grades_request.text)
        else:
            self.logger.error(f"Failed to fetch grades {grades_request.status_code}")


    def schedule(self):
        """
        gets the schedule of the student
        """
        self.logger.info("Getting schedule")
        self.login()
        schedule_url = self.init_url + "schedule"
        schedule_request = self.session.get(schedule_url, headers=self.headers)

        if schedule_request.status_code == 200:
            self.logger.debug(f"Schedule fetched successfully {schedule_request.text}")
            
        else:
            self.logger.error(f"Failed to fetch schedule {schedule_request.status_code}")
