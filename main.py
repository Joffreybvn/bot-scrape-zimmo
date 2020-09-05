import re
from src.scrappers.zimmo import Scrapper
from src import Collector

# What is "main": https://docs.python.org/fr/3/library/__main__.html
if __name__ == "__main__":
    Collector().start()

    """result = Scrapper("https://www.zimmo.be/fr/le%20roeulx-7070/a-vendre/maison/JP07D/").get_data()
    print(result)"""

