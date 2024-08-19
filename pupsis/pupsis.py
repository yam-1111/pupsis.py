from pupsis.utils.logs import Logger


class pupSIS:
    def __init__(
        self,
        student_number: str,
        student_birthdate: str,
        password: str,
        # utility stuff
        headers: dict = None,
        screenshot: bool = False,
    ):
        self.student_number = student_number
        self.student_birthdate = student_birthdate.split("/")
        self.password = password
        self.headers = headers
        self.screenshot = screenshot

        # birthdate
        self.birthdate_month = self.student_birthdate[0]
        self.birthdate_day = self.student_birthdate[1]
        self.birthdate_year = self.student_birthdate[2]

    @property
    def csrf_token(self):
        pass
