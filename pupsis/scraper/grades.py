
from selectolax.lexbor import LexborHTMLParser
from pupsis.logs import Logger
import re


class dictWrapper:
    """
    Wraps the dictionary into attributes

    ------
    Args:
        kwargs : dictionary values

    Returns:
        object : returns the object with attributes
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        return f"<{self.Semester} term {self.Academic_Year}>"

class Grade:
    """
    Parses the html data from the pupSIS grades page
    """
    def __init__(self, html_data: str):
        self.html_data = html_data

        #utilities
        self.grades = []
        self.infos = []
        self.header = []
        self.parse

    @property
    def parse(self):
        """
        extracts the data from the html string texts and stores on the lists

        ------
        Returns:
            list : returns class arrays (grades, infos, header)
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
                            tail = [x.text()for x in divs.css("dd")]
                            temp_infos.update(dict(zip(head, tail)))
                        else:
                            for table in divs.css("table"):
                                for x in table.iter():
                                    if x.tag == "thead":
                                        for j in x.iter():
                                            t_head = [(k.text().replace(" ", "_"))for k in j.iter()]
                                    if x.tag == "tbody":
                                        for j in x.iter():
                                            t_rows = [k.text() if k.text(strip=True) != "" else None for k in j.iter()]
                                            temp_grades.append(dict(zip(t_head, t_rows)))

                            if temp_infos:
                                self.infos.append(temp_infos)

                            if temp_grades:
                                self.grades.append(temp_grades)

                if secondary.attrs['class'] == "card-header":
                    pattern = r'School Year (\d{4}).*?(First|Second|Summer)'
                    match = re.search(pattern, secondary.text(strip=True))
                    self.header.append({
                        "Academic_Year" : match.group(1), "Semester" : match.group(2)
                    })

    @property
    def convert_to_dict(self):
        """
        merges all the array and return into dictionary

        ------
        Returns : list(dicts(combined_data))
        """
        combined_data = []
        combined_data = self.header.copy()
        for index, i in enumerate(self.infos): 
            for key, item in i.items():
                combined_data[index].update({key : item})
                combined_data[index].update({"grades" : self.grades[index]})
        return combined_data

    # functions
    def all(self):
        """
        pulls all the grades from start to latest
        in descending order

        ------
        Returns : list(<grades_obj>)
        """
        datas = [dictWrapper(**dict_obj) for dict_obj in self.convert_to_dict]
        return datas

    def latest(self):
        """
        pulls the latest academic semester grades
         
        ------
        Returns : <latest grades_obj>
        """
        return dictWrapper(**self.convert_to_dict[0])
    
    def is_complete(self, consider_p_grades=False, semester=0):
        """
        checks if the final grades from the latest semester in pupSIS are complete
        
        ------
        Args:
            consider_p_grades : (bool) 'P' consider 'P' as complete
            semester : (int) default is 0 [latest academic semester]

        Returns :
            is_complete : (bool) checks if grades are completed
        """

        for i in self.all()[semester].grades:
            if consider_p_grades:
                if i['Final_Grade'] is None:
                    return False
            else:
                if i['Final_Grade'] is None or i['Final_Grade'] == 'P':
                    return False
        return True

    
        