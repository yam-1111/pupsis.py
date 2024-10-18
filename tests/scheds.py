from pupsis import PUPSIS
from os import getenv
from dotenv import load_dotenv

load_dotenv()


# credentials can be optional, if loading local file
studs = PUPSIS(
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

schedule = studs.schedule(schedule_filename=getenv("SCHEDULE_FILEPATH"))


# load from sis
# schedule = studs.schedule()

print(schedule.body)
print(schedule.get_schedule())

