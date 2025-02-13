from selectolax.lexbor import LexborHTMLParser
from pupsis.utils.logs import Logger
import re


class GradeEntry:
    """Wraps a grade entry dictionary into an object with attribute access."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"<{self.Subject_Code}>"

class GradesWrapper:
    """Wraps the dictionary into attributes, including grades as objects."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "grades" and isinstance(value, list):
                # Convert each dict to GradeEntry
                self.grades = [GradeEntry(**grade) for grade in value]  
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"<{self.Semester} term {self.Academic_Year}>"



class Grade:
    """Parses the HTML data from the pupSIS grades page.

    Attributes:
        html_data (str): The HTML data as a string.

    Returns:
        latest(): Returns the latest semester grades.
        all(): Returns all semester grades.

    """
    def __init__(self, html_data: str):
        self.html_data = html_data

        # Utilities
        self.grades = []
        self.infos = []
        self.header = []
        self.parse

    @property
    def parse(self):
        """Extracts data from the HTML string and stores it in lists.

        Attributes:
            grades (list): Parsed grades data.
            infos (list): Parsed info data.
            header (list): Parsed header data.
        """
        tree = LexborHTMLParser(self.html_data)
        user_grades = tree.css("div.card-theme")
        for main in user_grades:
            for secondary in main.iter():
                temp_infos = {}
                temp_grades = []
                if secondary.attrs["class"] == "card-body":
                    for index, divs in enumerate(secondary.iter()):
                        if divs.css("dt") and divs.css("dd"):
                            head = [(x.text()).replace(" ", "_") for x in divs.css("dt")]
                            tail = [x.text() for x in divs.css("dd")]
                            temp_infos.update(dict(zip(head, tail)))
                        else:
                            for table in divs.css("table"):
                                for x in table.iter():
                                    if x.tag == "thead":
                                        for j in x.iter():
                                            t_head = [(k.text().replace(" ", "_")) for k in j.iter()]
                                    if x.tag == "tbody":
                                        for j in x.iter():
                                            t_rows = [k.text() if k.text(strip=True) != "" else None for k in j.iter()]
                                            temp_grades.append(dict(zip(t_head, t_rows)))

                            if temp_infos:
                                self.infos.append(temp_infos)

                            if temp_grades:
                                self.grades.append(temp_grades)

                if secondary.attrs["class"] == "card-header":
                    pattern = r'School Year (\d{4}).*?(First|Second|Summer)'
                    match = re.search(pattern, secondary.text(strip=True))
                    self.header.append({
                        "Academic_Year": match.group(1),
                        "Semester": match.group(2)
                    })

    @property
    def convert_to_dict(self):
        """Merges all arrays and returns them as a list of dictionaries.

        Returns:
            list: A list of dictionaries containing combined data.
        """
        combined_data = []
        combined_data = self.header.copy()
        for index, i in enumerate(self.infos): 
            for key, item in i.items():
                combined_data[index].update({key: item})
                combined_data[index].update({"grades": self.grades[index]})
        return combined_data

    def all(self):
        """Retrieves all grades from the start to the latest in descending order.

        Returns:
            list: A list of all semester grades from start to latest.
        """
        datas = [GradesWrapper(**dict_obj) for dict_obj in self.convert_to_dict]
        return datas

    def latest(self):
        """Retrieves the latest academic semester grades.

        Returns:
            GradesWrapper: An instance of the GradesWrapper class containing the latest semester grades
        """
        return GradesWrapper(**self.convert_to_dict[0])
    
    def is_complete(self, consider_p_grades=False, semester=0):
        """Checks if the final grades from the latest semester in pupSIS are complete.

        Attributes:
            consider_p_grades (bool): Whether to consider 'P' as a complete grade.
            semester (int): The semester to check (default is 0 for the latest semester).

        Returns:
            bool: True if the grades are complete, False otherwise.
        """
        for i in self.all()[semester].grades:
            if consider_p_grades:
                if i["Final_Grade"] is None:
                    return False
            else:
                if i["Final_Grade"] is None or i["Final_Grade"] == "P":
                    return False
        return True