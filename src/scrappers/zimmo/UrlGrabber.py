
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")


class UrlGrabber(Thread):

    def __init__(self, province: str):
        """
        Scrap the urls of all advertisement's webpage and return it to
        the Manager.

        :type province: str
        """

        Thread.__init__(self)
        self.source = f"https://www.zimmo.be/fr/province/{province}/a-vendre/?pagina=%s#gallery"
        self.urls = []

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

    def __grab(self) -> None:
        """
        Grab the urls of the adverts from the source link.
        This method is called by run() and is threaded.
        """

        i = 0
        is_complete = False

        while not is_complete:
            i += 1

            # Fetch the webpage
            driver.get(self.source % i)

            # Check if there are adverts
            if not driver.find_elements(By.CLASS_NAME, "col-sm-7"):

                # Append all advertisement's links
                links = driver.find_elements_by_class_name("property-item_link")
                for link in links:
                    self.urls.append(link.get_attribute('href'))

            # If the grabber reach the last page, stop the loop
            else:
                is_complete = True

