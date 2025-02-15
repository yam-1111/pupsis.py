# example of getting the latest grades of the student

from pupsis import PUPSIS
from os import getenv
from dotenv import load_dotenv


# optional to use .env file, can be hardcoded
load_dotenv()
pupsis = PUPSIS(
    # PUP student number 20xx-xxxxx-XX-0 i.e 2024-12345-MN-0
    student_number = getenv("STUDENT_NUMBER"),
    # student birthdate format M/DD/YYYY i.e 1/1/2000
    student_birthdate=getenv("STUDENT_BIRTHDAY"),
    # pupsis student password
    password= getenv("PASSWORD"),
    # set logging level details i.e None, "DEBUG", "INFO", "WARNING", "ERROR"
    # default = None
    loglevel=getenv("LOG_LEVEL"),
    # add custom delay between requests by default = 2
    request_delay=int(getenv("REQUEST_DELAY"))
)
latest_grades = pupsis.grades().latest()
sched = pupsis.schedule()

print(sched.__dict__)
for x in latest_grades.grades:
    print(f"{x.Faculty_Name} - {x.Subject_Code} - {x.Description}  - {x.Final_Grade} {x.Grade_Status}")

print(f"Total Units: {latest_grades.total_units}")