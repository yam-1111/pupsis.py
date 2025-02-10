import hishel
from selectolax.lexbor import LexborHTMLParser
from pupsis.utils.logs import Logger
from pupsis.errors import LoginError, MultipleLoginAttempt
from typing import Optional
import httpx


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
        self.urls = [
            "https://sis8.pup.edu.ph/student/",
            "https://sis1.pup.edu.ph/student/",
            "https://sis2.pup.edu.ph/student/",
        ]
        self.client = hishel.CacheClient(controller=controller, storage=storage)

    def __client(self, method: str, endpoint: str, data: Optional[dict] = None):
        """
        Helper method for making GET or POST requests with retry logic for multiple SIS URLs using hishel.
        """
        timeout = 100.0  # Set timeout to 100 seconds

        for url in self.urls:
            try:
                full_url = url + endpoint
                self.logger.debug(f"Making {method} request to {full_url} with timeout {timeout}s")

                if method == 'GET':
                    response = self.client.get(full_url, timeout=timeout)
                elif method == 'POST':
                    response = self.client.post(full_url, data=data, timeout=timeout)

                elapsed_time = response.elapsed.total_seconds()
                if elapsed_time > 80:
                    self.logger.warning(f"Request to {full_url} took {elapsed_time}s, nearing timeout limit!")

                response.raise_for_status()  # Raises exception for non-2xx responses
                return response
            except httpx.TimeoutException:
                self.logger.error(f"Request to {full_url} timed out after {timeout}s.")
            except httpx.RequestError as e:
                self.logger.warning(f"Failed to make {method} request to {url}: {e}")
                continue  # Try the next URL

        self.logger.error(f"Failed to make {method} request to all available SIS URLs.")
        raise LoginError(f"Request failed after trying all SIS URLs.")

    def __get_csrf_token(self):
        self.logger.info("Extracting CSRF token")
        response = self.__client('GET', "")
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
        response = self.__client('POST', "", data=payload)
        refresh_header = response.headers.get("Refresh")
        if refresh_header == '0;url=https://sis8.pup.edu.ph/student/authentication/lockaccount':
            raise MultipleLoginAttempt()
        if refresh_header == '0;url=https://sis8.pup.edu.ph/student/':
            self.logger.error(f"Failed to login: {response.status_code}")
            raise LoginError("Incorrect login credentials")
        self.logger.info("Login successful")

    def get_grades(self):
        self.__login()
        response = self.__client('GET', "grades")
        if response.status_code == 200:
            return response.text
        self.logger.error(f"Failed to fetch grades: {response.status_code}")
        return None

    def get_schedule(self, save_html: Optional[bool] = False):
        self.__login()
        response = self.__client('GET', "schedule")
        if response.status_code == 200:
            return response.text
        self.logger.error(f"Failed to fetch schedule: {response.status_code}")
        return None
