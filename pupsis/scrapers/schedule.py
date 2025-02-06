from selectolax.lexbor import LexborHTMLParser
from datetime import datetime
from re import search
from pupsis.utils.logs import Logger


class scheduleWrapper:
    def __init__(
        self,
        semester: str,
        subject_code: str,
        subject_description: str,
        section: str,
        units: str,
        lab: str,
        lec: str,
        start_time: str,
        end_time: str,
        faculty_name: str,
    ):
        self.semester = semester
        self.subject_code = subject_code
        self.subject_description = subject_description
        self.section = section
        self.units = units
        self.lab = lab
        self.lec = lec
        self.start_time = start_time
        self.end_time = end_time
        self.faculty_name = faculty_name

    def __repr__(self):
        return f"{self.subject_code} - {self.subject_description} - {self.section} - {self.start_time} - {self.end_time} - {self.faculty_name}"


class Schedule:
    def __init__(self, html_data: str, log_file=None, log_level=None):
        self.html_data = html_data
        self.head
        self.body
        if log_level:
            self.logger = Logger("Schedule", log_file=log_file, level=log_level)
        # self.sched()

    @property
    def school_year(self):
        tree = LexborHTMLParser(self.html_data)
        try:
            pattern = r'\b\d{4}\b'
            return search(pattern, tree.css_first("section h1").text(strip=True)).group()
        except Exception as e:
            self.logger.error(f"Error extracting the school year {e}")

    @property
    def semester(self):
        tree = LexborHTMLParser(self.html_data)
        try:
            return tree.css_first("section h1").text(strip=True)
        except Exception as e:
            self.logger.error(f"Error extracting the semester {e}")

    @property
    def head(self):
        tree = LexborHTMLParser(self.html_data)
        user_sched = tree.css("div.card-body div.table-responsive table thead tr")
        try:
            return [x.text() for x in user_sched[0].css("th")]
        except Exception as e:
            self.logger.error(f"Error extracting the schedule head {e}")

    @property
    def body(self):
        tree = LexborHTMLParser(self.html_data)
        sched = []
        user_sched = tree.css("div.card-body div.table-responsive table tbody tr")
        for tr in user_sched:
            temp_sched = []
            for index, td in enumerate(tr.css("td")):

                # extract the subject_code
                if index in range(0, 5):
                    temp_sched.append(td.text(strip=True))

                if index == len(tr.css("td")) - 1:
                    last_td = (td.text(strip=True)).split(" - ")

                    # extract the course section
                    temp_sched.append(last_td[1])

                    # extract the schedule
                    day, *times = last_td[2].replace("Faculty:", "").split(" ")

                    # extract the day and time
                    day_map = {
                        "M": "Monday",
                        "T": "Tuesday",
                        "W": "Wednesday",
                        "TH": "Thursday",
                        "F": "Friday",
                        "S": "Saturday",
                        "SUN": "Sunday",
                    }
                    sched_time = []
                    day = day.split("/")
                    times = times[0].split("/")

                    for day_abbr, time_abbr in zip(day, times):
                        day = day_map[day_abbr]
                        start_time_str, end_time_str = time_abbr.split("-")
                        sched_time.append((day, start_time_str, end_time_str))
                    temp_sched.append(sched_time)
                    # get the faculty name
                    faculty_name = td.css_first("font").text(strip=True)
                    if faculty_name in "Faculty:":
                        temp_sched.append(None)
                    else:
                        temp_sched.append(faculty_name.replace("Faculty: ", ""))

            sched.append(temp_sched)
        return sched

    # class function
    def get_schedule(self):
        """exports the schedule to a list of scheduleWrapper

        Returns:
            list: list of scheduleWrapper
        """
        pass