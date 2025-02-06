from pupsis import PUPSIS

from os import getenv, path
from dotenv import load_dotenv
import sys


sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "..")))

def main():
    load_dotenv()
    pupsis = PUPSIS(
       # PUP student number 20xx-xxxxx-XX-0 i.e 2024-12345-MN-0
        student_number = getenv("STUDENT_NUMBER"),
        # student birthdate format M/DD/YYYY i.e 1/1/2000
        student_birthdate=getenv("STUDENT_BIRTHDAY"),
        # pupsis student password
        password= getenv("PASSWORD"),
        # set logging level details i.e None, DEBUG, INFO, WARNING, ERROR
        # default = None
        # loglevel="INFO"
    )
    latest_grades = pupsis.grades().latest()
    headers = pupsis.grades().header

    for x in latest_grades.grades:
        ctx = ""
        for j in x.keys():
            ctx += f"{x[j]} | "
        print(ctx)

if __name__ == "__main__":
    main()