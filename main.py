import re
from src.scrappers.zimmo import Scrapper
from src import Collector
from src.cleaner import Merger

# What is "main": https://docs.python.org/fr/3/library/__main__.html
if __name__ == "__main__":
    Collector().start()
    #Merger().merge()
