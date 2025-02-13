
import re
from typing import NewType

StudentNumber = NewType("StudentNumber", str)

def validate_student_number(value: str) -> StudentNumber:
    if not re.fullmatch(r"20\d{2}-\d{5}-[A-Z]{2}-\d", value):
        raise ValueError(f"InvalidStudentNumber: {value} (Expected format: 20XX-xxxxxx-XX-x)")
    return StudentNumber(value)


def validate_student_birthdate(value: str) -> str:
    if not re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", value):
        raise ValueError(f"InvalidBirthdate: {value} (Expected format: M/DD/YYYY)")
    return value