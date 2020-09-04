
from src.scrappers.zimmo.Utils import Scrap, ScrapMoreInfo, ScrapSurface

import re
from threading import Thread
from typing import Union
from bs4 import BeautifulSoup, Tag
from selenium import webdriver


class Scrapper(Thread):

    def __init__(self, url):
        """
        Scrap all data from a given advertisement webpage and return it to
        the Manager.
        """

        super().__init__()

        self.scrappers = [
            Scrap(function=self.__scrap_locality),  # Locality
            Scrap(function=self.__scrap_property_type),  # Type of property
            Scrap(function=self.__scrap_property_subtype),  # Subtype of property
            Scrap(function=self.__scrap_price),  # Price
            Scrap(function=self.__scrap_sale_type),  # Sale type
            Scrap(function=self.__scrap_rooms_number),  # Room number
            ScrapSurface(function=self.__scrap_regex_value, title='Surface habitable'),  # Area
            Scrap(function=self.__scrap_kitchen),  # Kitchen equipment
            Scrap(function=self.__scrap_furnished),  # Furnished
            Scrap(function=self.__scrap_open_fire),  # Open fire
            ScrapMoreInfo(function=self.__scrap_v_mark, title='Terrasse'),  # Terrace
            Scrap(function=self.__scrap_terrace_area),  # Terrace Area
            ScrapMoreInfo(function=self.__scrap_v_mark, title='Jardin'),  # Garden
            Scrap(function=self.__scrap_garden_area),  # Garden Area
            ScrapSurface(function=self.__scrap_regex_value, title='Surface construite'),  # Surface of the land
            ScrapSurface(function=self.__scrap_regex_value, title='Superficie du terrain'),  # Plot of land
            ScrapMoreInfo(function=self.__scrap_regex_value, title='Construction', regex=r"(?P<number>\d)-façades"),  # Facades
            ScrapMoreInfo(function=self.__scrap_v_mark, title='Terrasse'),  # Swimming Pool
            ScrapMoreInfo(function=self.__scrap_building_state)  # Building
        ]

        self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        #self.driver = webdriver.Chrome("/Users/noahalvarezgonzalez/Drivers/chromedriver")
        self.url = url
        self.data = []
        self.soup = None

    def get_data(self):

        if not self.data:
            self.scrap()

        return self.data

    def scrap(self):

        # Fetch the page
        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, "lxml")

        # Scrap the data
        for scrap in self.scrappers:
            result = scrap.function(scrap.tag, scrap.clasz, scrap.title, scrap.regex)

            # Store it
            self.data.append(result)

        self.driver.close()

    def __scrap_locality(self, *args) -> Union[str, None]:

        title = self.__get_text(self.__scrap_field('h2', {"class": "section-title"}))

        if title:
            regex = re.search(r"((\d){4} (?P<city>.+)$)", title.strip())

            if regex:
                return regex.group("city")

        return None

    def __scrap_garden_area(self, *args):
        return None

    def __scrap_terrace_area(self, *args):
        return None

    def __scrap_property_type(self, *args):
        return None

    def __scrap_property_subtype(self, *args):
        return "later"

    def __scrap_price(self, *args) -> Union[str, None]:
        """Scrap the price."""

        tag = self.__get_text(self.__scrap_field('div', {"class": "price-box"}))

        # TODO: Pourquoi un regex si restrictif ?
        if tag:
            price = re.search(r"(?P<price>([0-9]{0,3}[.]?[0-9]{0,3}[.]?[0-9]{1,3})$)", tag.strip())

            if price:
                return price.group("price")

        return None

    def __scrap_sale_type(self, *args) -> Union[str, None]:
        """Scrap the sale type."""
        sale = self.__scrap_field('div', {"class": "price-box"})

        if sale:
            icon = sale.find("svg")

            if not icon:
                return "notariale"
            else:
                return "agence"
        return None

    def __scrap_rooms_number(self, *args):
        # TODO: implement rooms number
        return 0

    def __scrap_kitchen(self, *args):
        # TODO: Better filter
        return self.__scrap_description(r".*([Cc]uisine [Eée]quipée).*")

    def __scrap_furnished(self, *args) -> bool:
        """Scrap if the house has furniture or not, by looking on the description."""

        if self.__scrap_v_mark('div', 'col-xs-7 info-name', 'Meublé'):
            return True

        else:
            return self.__scrap_description(r".*([mM]eublé|[mM]eubels).*")

    def __scrap_open_fire(self, *args) -> bool:
        """Scrap if there's an open fire or not, by looking on the description."""

        return self.__scrap_description(r".*([fF]eu [oO]uvert|[oO]pen [hH]aard).*")

    """ SPECIAL METHODS --------------------------------------------
    The following methods are used only to scrap one specific things.
    They can't be factorized. They use Basics and Commons methods to
    work.
    """

    def __scrap_building_state(self, tag, attributes, *args) -> Union[str, None]:
        """Scrap the state of the building."""
        # TODO: Implement more guessing about if a house is old or to be renovated

        # The state can be found from two fields:
        fields = [
            ('Année de rénovation', "new"),
            ('Année de construction', 'old')
        ]

        # Loop through all field
        for field in fields:
            result = self.__scrap_field_value(tag, attributes, field[0])

            # If a field exists, return the corresponding data
            if result:
                return field[1]

        # Return None if no data was scrapped
        return None

    """ COMMON METHODS --------------------------------------------
    The following methods are reused to scrap multiple kind of
    data's. They use the Basic methods to work.
    """

    def __scrap_description(self, regex, *args) -> bool:
        """Scrap the description and look for match."""

        # Scrap the description
        description = self.__get_text(self.__scrap_field('p', {"class": "description-block"}))

        # Find a match for the given regex
        if description and re.match(regex, description, re.DOTALL):
            return True
        else:
            return False

    def __scrap_regex_value(self, tag, attributes, text, regex) -> Union[str, None]:
        """Scrap a value through a regex."""

        # Scrap the value's text
        result = self.__get_text(self.__scrap_field_value(tag, attributes, text))

        # If the text is not empty, apply regex
        if result:
            regex = re.search(regex, result)

            # If the regex is not empty, return its value
            if regex:
                return regex.group("number")

        # Return None if no value was found
        return None

    def __scrap_v_mark(self, tag, attributes, text, *args) -> bool:
        """
        Scrap a value with a V mark.
        Used for: Swimming pool, garden.
        """

        # Scrap the value
        result = self.__scrap_field_value(tag, attributes, text)

        # Check if there's a V mark in the field
        if result and result.find('i', {"class": "zf-icon icon-check yes"}):
            return True

        # Return False if not
        return False

    """ BASICS METHODS --------------------------------------------
    The following methods are the basic blocks used to create other
    scrapping functions.
    """

    def __scrap_field(self, tag, attributes, text=None) -> Union[Tag, None]:
        """Scrap a field and return it."""

        return self.soup.find(tag, attributes, string=text)

    def __scrap_field_value(self, tag, attributes, text) -> Union[Tag, bool]:
        """Scrap a field by its title and return the value of this field."""

        # Retrieve the field containing the title.
        title = self.__scrap_field(tag, attributes, text)

        # If it exists, return its value.
        if title:
            return title.find_next('div')

        return False

    @staticmethod
    def __get_text(tag: Tag) -> Union[str, bool]:
        """Retrieve and return the text from a given BeautifulSoup Tag."""

        # If the tag is not empty, return its content.
        if tag:
            return tag.get_text()

        return False
