
from src.scrappers import Request, WebDriver

from threading import Thread
from bs4 import BeautifulSoup


class UrlGrabber(Thread):

    base_url = "https://www.zimmo.be"

    def __init__(self, province: str):
        """
        Scrap the urls of all advertisement's webpage and return it to
        the Manager.

        :type province: str
        """

        Thread.__init__(self)
        print(f'[+] UrlGrabber: Start grabbing for {province}')

        self.source = f"https://www.zimmo.be/fr/province/{province}/a-vendre/?pagina=%s#gallery"
        self.urls: list = []
        self.driver = WebDriver()

    def get_urls(self):
        """Return a list of all urls of the given province."""

        # If the urls list is empty, start the grabber
        if not self.urls:
            self.run()

        # Then return the urls
        return self.urls

    def run(self):
        """Launch the threaded execution of this class."""
        self.__grab()
        self.driver.close()

    def __grab(self) -> None:
        """
        Grab the urls of the adverts from the source link.
        This method is called by run() and is threaded.
        """

        i = 307
        is_complete = False

        while not is_complete:
            i += 1

            # Fetch the page
            # response = Request().get(self.source % i)
            if self.driver.get(self.source % i) is not None:
                self.soup = BeautifulSoup(self.driver.page_source(), "lxml")

                # Check if there are adverts
                if not self.soup.find('div', {"class": 'alert alert-danger'}):

                    # Append all advertisement's links
                    links = self.soup.find_all('a', {"class": 'property-item_link'}, href=True)
                    for link in links:
                        self.urls.append(f"{UrlGrabber.base_url}{link.get('href')}")

                # If the grabber reach the last page, stop the loop
                else:
                    is_complete = True
