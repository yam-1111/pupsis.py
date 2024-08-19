
from pupsis.rest import pupSIS
import logging

user = pupSIS(
    student_number = "2022-08882-MN-0",
    student_birthdate="8/20/2004",
    password="Anthony_8202004",
)

grades = user.grades().latest()

print('grades complete? ' , user.grades().is_complete())
for x in grades.grades:
    print(x['Subject_Code'], x['Final_Grade'], x['Faculty_Name'])



