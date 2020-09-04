
import concurrent
from concurrent.futures import wait
from concurrent.futures import ThreadPoolExecutor
from src.scrappers.zimmo import Scrapper, UrlGrabber


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
        self.urls: list = []
        self.retrieve_urls()

    def retrieve_urls(self):
        """Retrieve the urls of all selling advertisement from zimmo.be."""

        urls = self.__thread_call(self.url_grabber, Manager.provinces, 10)
        for url in urls:
            print(url.result())

        # TODO: Store the urls in self.urls

    @staticmethod
    def __thread_call(func, sources, max_workers):
        """
        Call a given function ('func') multiple time simultaneously.

        :param func: The function to start multiple simultaneous instances.
        :param sources: The list of provinces
        :param max_workers: the maximum instances to start at once.

        :return: An iterator with the content returned by the 'func' instances.
        """

        # Start simultaneously multiple instances of the given function
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, entry) for entry in sources]

            # Return an iterator of lists
            return concurrent.futures.as_completed(futures)

    @staticmethod
    def url_grabber(province):
        return UrlGrabber(province).get_urls()

