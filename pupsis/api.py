import hishel
import logging
from selectolax.lexbor import LexborHTMLParser
from pupsis.utils.logs import Logger
from pupsis.errors import LoginError, MultipleLoginAttempt
from typing import Optional


# cache controllers
controller = hishel.Controller(
    allow_heuristics=True
)

storage = hishel.FileStorage(
    ttl=30,
    check_ttl_every=10,
)


# api requester
class APIRequester:
    def __init__(
        self,
        student_number: str,
        student_birthdate: str,
        password: str,
        logfile: Optional[str] = None,
        loglevel: Optional[str] = "INFO",
    ):
        self.student_number = student_number
        self.student_birthdate = student_birthdate.split("/")
        self.password = password
        self.logger = Logger("APIRequester", log_file=logfile, level=loglevel)
        self.base_url = "https://sis8.pup.edu.ph/student/"
        self.client = hishel.CacheClient(controller=controller, storage=storage)

    def __get_csrf_token(self):
        self.logger.info("Extracting CSRF token")
        response = self.client.get(self.base_url)
        tree = LexborHTMLParser(response.text)
        csrf = [tree.css_first(selector).attrs["value"] for selector in ["input[name='csrf_token']", "input#tempcsrf"]]
        self.logger.debug(f"CSRF token extracted: {csrf}")
        return tuple(csrf)

    def __login(self):
        self.logger.info("Logging in to SIS")
        self.logger.debug(f"Credentials : {self.student_number} | {self.student_birthdate} | {self.password}")
        csrf = self.__get_csrf_token()
        payload = {
            "csrf_token": csrf[0],
            "csrf_token": csrf[1],
            "studno": self.student_number,
            "SelectMonth": self.student_birthdate[0],
            "SelectDay": self.student_birthdate[1],
            "SelectYear": self.student_birthdate[2],
            "password": self.password,
            "Login": "Sign in",
        }
        response = self.client.post(self.base_url, data=payload)
        
        if response.status_code == 200:
            refresh_header = response.headers.get("Refresh")
            if refresh_header == '0;url=https://sis8.pup.edu.ph/student/authentication/lockaccount':
                raise MultipleLoginAttempt()
            if refresh_header == '0;url=https://sis8.pup.edu.ph/student/':
                self.logger.error(f"Failed to login: {response.status_code}")
                raise LoginError("Incorrect login credentials")
            self.logger.info("Login successful")
        else:
            self.logger.error(f"Failed to login: {response.status_code}")
            raise LoginError("Login failed")

    def get_grades(self):
        self.__login()
        response = self.client.get(self.base_url + "grades")
        if response.status_code == 200:
            return response.text
        self.logger.error(f"Failed to fetch grades: {response.status_code}")
        return None

    def get_schedule(self, save_html: Optional[bool] = False):
        self.__login()
        response = self.client.get(self.base_url + "schedule")
        if response.status_code == 200:
            return response.text
        self.logger.error(f"Failed to fetch schedule: {response.status_code}")
        return None
