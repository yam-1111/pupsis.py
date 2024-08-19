from selectolax.lexbor import LexborHTMLParser
from pupsis.utils.logs import Logger

class Status:
    def __init__(self, html_data : str):
        self.html_data = html_data

    