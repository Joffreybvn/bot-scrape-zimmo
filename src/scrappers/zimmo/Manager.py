
# from src.scrappers.zimmo import Scrapper, UrlGrabber
from UrlGrabber import UrlGrabber


class Manager:

    # Provinces to scrap
    provinces = [
        "anvers",
        "brabant-flamand",
        "brabant-wallon",
        "flandre-occidentale",
        "flandre-orientale",
        "hainaut",
        "liege",
        "limbourg",
        "luxembourg",
        "namur",
        "region-de-bruxelles-capitale"
    ]

    def __init__(self):
        """
        The Manager class coordinate the UrlGrabber and the Scrapper:

        It retrieve the URLs given by an UrlGrabber, then instantiate multiple
        threaded Scrappers and return their result to the Cleaner.
        """
        self.urls : list = []

        grabber = UrlGrabber(Manager.provinces[0])
        grabber.start()

    def retrieve_urls(self):
        pass


Manager()
