# pupsis.py

[![Hippocratic License HL3-CL](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl.html)

Unofficial Python API for the PUP Student Information System (PUPSIS).

⚠️ This project is **not affiliated with, endorsed by, or officially supported by PUP**. It is an independent tool designed to help students automate checking of grades and schedule.  






## 🚨 Anti-Abuse Notice
This project is **NOT** intended for aggressive scraping, bot automation, or any activity that could harm PUPSIS.  
We strongly discourage **unauthorized modifications** that violate ethical and legal boundaries.  
If you see anyone using this tool irresponsibly, please report the misuse.  


## 🚨 Responsible & Ethical Usage

> **⚠️ AVOID Excessive Requests**  
> Sending too many requests in a short period **can slow down or disrupt** the SIS, making it harder for fellow students to access their data. Please use this tool responsibly to avoid negatively impacting the system.  

> **⚠️ Ethical Use Only**  
> This library is intended for **personal and ethical** use. Any unauthorized access, data scraping beyond personal use, or violation of PUP policies is strictly prohibited.  


## 🛠 Dependencies  
- [selectolax](https://selectolax.readthedocs.io/)  
- [httpx](https://www.python-httpx.org/)
- [hishel](https://hishel.com/)  

## 🚀 How to use?

```bash
pip install git+https://github.com/yam-1111/pupsis.py
```

### Usage example

#### Check if grades in SIS is complete

```python
from pupsis import PUPSIS

user = PUPSIS(
    student_number="YYYY-XXXXX-XX-0",  # Replace with your student number i.e 20XX-XXXXX-MN-0
    student_birthdate="MM/DD/YYYY",   # Replace with your birthdate i.e 1/2/2003
    password="YourSecurePassword",    # Replace with your password
)

# this requests grades section on SIS
grades = user.grades()

print(f"Grade complete: {grades.is_complete()}")
```

#### Get all the grades from the latest semester

```python
# example of getting the latest grades of the student

from pupsis import PUPSIS
from os import getenv
from dotenv import load_dotenv

# use dotnenv to protect credentials (optional)
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
    loglevel="INFO"
)

# output the latest semester only
latest_grades = pupsis.grades().latest()

# iterate the grades
for x in latest_grades.grades:
    print(f"{x.Faculty_Name} - {x.Subject_Code} - {x.Description}  - {x.Final_Grade} {x.Grade_Status}")
```


