import hishel
from selectolax.lexbor import LexborHTMLParser
from pupsis.utils.logs import Logger
from pupsis.errors import LoginError, MultipleLoginAttempt
from typing import Optional
import httpx
import time, random


# cache controllers
controller = hishel.Controller(
    allow_heuristics=True,
    force_cache=True,
)

storage = hishel.FileStorage(
    ttl=30,
    check_ttl_every=10,
)


class APIRequester:
    def __init__(self, 
                 
                student_number: str, 
                student_birthdate: str, 
                password: str, 

                # header
                headers: Optional[dict] = None,

                # logging utility stuff
                logfile: Optional[str] = None, 
                loglevel: Optional[str] = "INFO",

                # implement delay
                request_delay: Optional[int] = 0

                ):
        self.student_number = student_number
        self.student_birthdate = student_birthdate.split("/")
        self.password = password
        self.headers = headers
        self.logger = Logger("APIRequester", log_file=logfile, level=loglevel)
        self.urls = [
            "https://sis8.pup.edu.ph/student/",
            "https://sis1.pup.edu.ph/student/",
            "https://sis2.pup.edu.ph/student/",
        ]

        # request delay
        self.request_delay = request_delay

        # cache controllers
        self.client = hishel.CacheClient(controller=controller, storage=storage)
        self.session_cookies = None  # Store cookies after login
        self.is_logged_in = False  

    def __client(self, method: str, endpoint: str, data: Optional[dict] = None):
        timeout = 100
        for url in self.urls:
            try:
                full_url = url + endpoint
                self.logger.debug(f"Making {method} request to {full_url} with timeout {timeout}s")

                if self.request_delay != 0:
                    self.logger.debug(f"Delaying request for {random.uniform(0.1, self.request_delay)}s")
                    time.sleep(random.uniform(0.1, self.request_delay))  # Prevents being detected as a bot

                if method == 'GET':
                    response = self.client.get(full_url, headers=self.headers, timeout=timeout)

                elif method == 'POST':
                    response = self.client.post(full_url, data=data, headers=self.headers, timeout=timeout)

                self.logger.debug(f"Response headers: {response.headers}")

                # Store cookies properly
                self.client.cookies.update(response.cookies)
                response.raise_for_status()  # Raises exception for non-2xx responses
                return response
            
            except httpx.TimeoutException:
                self.logger.error(f"Request to {full_url} timed out after {timeout}s.")
            except httpx.RequestError as e:
                self.logger.warning(f"Failed to make {method} request to {url}: {e}")
                continue  

        self.logger.error(f"Failed to make {method} request to all available SIS URLs.")
        raise LoginError(f"Request failed after trying all SIS URLs.")

    def __session_valid(self):
        """
        Checks if the session is still valid by requesting a protected page.
        """
        response = self.__client("GET", "dashboard")  # Assume dashboard requires authentication
        return response.status_code == 200
    
    def __get_csrf_token(self):
        self.logger.info("Extracting CSRF token")
        response = self.__client('GET', "")
        tree = LexborHTMLParser(response.text)
        csrf = [tree.css_first(selector).attrs["value"] for selector in ["input[name='csrf_token']", "input#tempcsrf"]]
        self.logger.debug(f"CSRF token extracted: {csrf}")
        return tuple(csrf)


    def __login(self):
        """Logs in only if the session is invalid."""
        if self.is_logged_in and self.__session_valid():
            self.logger.info("Already logged in, session is still valid.")
            return
        
        self.logger.info("Logging in to SIS")
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
            self.logger.error("Failed to login: Incorrect credentials")
            raise LoginError("Incorrect login credentials")

        self.logger.info("Login successful")
        self.is_logged_in = True

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
