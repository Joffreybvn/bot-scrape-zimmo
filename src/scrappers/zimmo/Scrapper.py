
import re
from threading import Thread
from typing import Union
from bs4 import BeautifulSoup, Tag
from selenium import webdriver

"""
************************definition of variables****************************** 
locality : str
type_of_property : house/appartment
subtype of property :
price : int (euros)
sale_type : by agency/notarial
Num_rooms : int
area : int (squared meters)
kitchen_equipment : none, equipped, fully equipped
furnished : yes/no
open_fire : yes/no
terrace : yes/no
    If yes, surface : int (squared meters)
garden
    if yes, surface : int (squared meters)
surface_land : int (squared meters)
surface_plot_land : int (squared meters)
number_of_facades : int
swimming_pool : yes/no
state_building : new/to be renovated 
******************************************************************************
"""

# Regex:
# facades: r"(?P<number>\d)-façades"


class Scrapper(Thread):

    attributes = [

        {  # 0 - default : num_rooms, kitchen_equipment, furnished,
            # is in //div @class="col-xs-7 info-name"
            "tag": 'div',
            "attributes": {
                "class": "col-xs-7 info-name",
                "text": ""
            },
            "sanitizer": "default"
        },
        {  # 1 - facade
            # is in //div @class="col-xs-7 info-name"
            "tag": 'div',
            "attributes": {
                "class": "col-xs-7 info-name",
                "text": "Construction"
            },
            "sanitizer": "facade"
        },
        {  # 2 - state_building
            # is in //div @class="col-xs-7 info-name"
            "tag": 'div',
            "attributes": {
                "class": "col-xs-7 info-name",
                "text": "Année de rénovation"
            },
            "sanitizer": "state_building"
        },
        {  # 3 - locality
            # is in //h2 @class="section-title"
            "tag": 'h2',
            "attributes": {
                "class": "section-title"
            },
            "sanitizer": "locality"
        },
        {  # 4 - price
            # is in //div @class="price-box"
            "tag": 'div',
            "attributes": {
                "class": "price-box",
            },
            "sanitizer": "price"
        },
        {  # 5 - sale_type
            # is in //div @class="price-box"
            "tag": 'div',
            "attributes": {
                "class": "price-box",
            },
            "sanitizer": "sale_type"
        },
    ]

    def __init__(self, url):
        """
        Scrap all data from a given advertisement webpage and return it to
        the Manager.
        """

        super().__init__()

        #self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.driver = webdriver.Chrome("/Users/noahalvarezgonzalez/Drivers/chromedriver")
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
        self.data = [
            self.__scrap_locality(),  # Locality
            self.__scrap_property_type(),  # Type of property
            self.__scrap_property_subtype(),  # Subtype of property
            self.__scrap_price(),  # Price
            self.__scrap_sale_type(),  # Sale type
            self.__scrap_rooms_number(),  # Room number
            self.__scrap_regex_value('div', 'col-xs-7 info-name', 'Surface habitable', r"(?P<number>\d*) m²"),  # Area
            self.__scrap_kitchen(),  # Kitchen equipment
            self.__scrap_furnished(),  # Furnished
            self.__scrap_open_fire(),  # Open fire
            self.scrap_v_mark('div', 'col-xs-7 info-name', 'Terrasse'),  # Terrace
            None,  # Terrace Area
            self.scrap_v_mark('div', 'col-xs-7 info-name', 'Jardin'),  # Garden
            None,  # Garden Area
            self.__scrap_regex_value('div', 'col-xs-7 info-name', 'Surface construite', r"(?P<number>\d*) m²"),  # Surface of the land
            self.__scrap_regex_value('div', 'col-xs-7 info-name', 'Superficie du terrain', r"(?P<number>\d*) m²"),  # Plot of land
            self.__scrap_regex_value('div', 'col-xs-7 info-name', 'Construction', r"(?P<number>\d)-façades"),  # Facades
            self.scrap_v_mark('div', 'col-xs-7 info-name', 'Piscine'),  # Swimming Pool
            self.__scrap_building_state('div', 'col-xs-7 info-name')  # Building state
        ]

        self.driver.close()

    def __scrap_locality(self) -> Union[str, None]:

        title = self.__get_text(self.__scrap_field('h2', {"class": "section-title"}))

        if title:
            regex = re.search(r"((\d){4} (?P<city>.+)$)", title.strip())

            if regex:
                return regex.group("city")

        return None

    def __scrap_property_type(self):
        pass

    def __scrap_property_subtype(self):
        return "later"

    def __scrap_price(self) -> Union[str, None]:
        """Scrap the price."""

        tag = self.__get_text(self.__scrap_field('div', {"class": "price-box"}))

        # TODO: Pourquoi un regex si restrictif ?
        if tag:
            price = re.search(r"(?P<price>([0-9]{0,3}[.]?[0-9]{0,3}[.]?[0-9]{1,3})$)", tag.strip())

            if price:
                return price.group("price")

        return None

    def __scrap_sale_type(self) -> Union[str, None]:
        """Scrap the sale type."""
        sale = self.__scrap_field('div', {"class": "price-box"})

        if sale:
            icon = sale.find("svg")

            if not icon:
                return "notariale"
            else:
                return "agence"
        return None

    def __scrap_rooms_number(self):
        # TODO: implement rooms number
        return 0

    def __scrap_kitchen(self):
        # TODO: Better filter
        return self.__scrap_description(r".*([Cc]uisine [Eée]quipée).*")

    def __scrap_furnished(self) -> bool:
        """Scrap if the house has furniture or not, by looking on the description."""

        if self.scrap_v_mark('div', 'col-xs-7 info-name', 'Meublé'):
            return True

        else:
            return self.__scrap_description(r".*([mM]eublé|[mM]eubels).*")

    def __scrap_open_fire(self) -> bool:
        """Scrap if there's an open fire or not, by looking on the description."""

        return self.__scrap_description(r".*([fF]eu [oO]uvert|[oO]pen [hH]aard).*")


    def __scrap_description(self, regex) -> bool:
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

    def scrap_v_mark(self, tag, attributes, text) -> bool:
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

    def __scrap_building_state(self, tag, attributes) -> Union[str, None]:
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

        # If the field doesn't exist, return False.
        return False

    @staticmethod
    def __get_text(tag: Tag) -> Union[str, bool]:
        """Retrieve and return the text from a given tag."""

        # If the tag is not empty, return its content.
        if tag:
            return tag.get_text()

        # Return false if not.
        return False
