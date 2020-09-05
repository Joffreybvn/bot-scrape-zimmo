
from src.scrappers.zimmo.Utils import Scrap, ScrapMoreInfo, ScrapSurface
from src.scrappers import Request

import re
from threading import Thread
from typing import Union
from bs4 import BeautifulSoup, Tag
from pandas.core.common import flatten


class Scrapper(Thread):

    def __init__(self, url):
        """
        Scrap all data from a given advertisement webpage and return it to
        the Manager.
        """
        super().__init__()

        self.scrappers = [
            Scrap(function=self.__scrap_locality),  # Locality
            Scrap(function=self.__scrap_property_type),  # Type and subtype of property
            Scrap(function=self.__scrap_price, tag='div', clasz='price-box'),  # Price
            Scrap(function=self.__scrap_sale_type, tag='div', clasz='price-box'),  # Sale type
            Scrap(function=self.__scrap_rooms_number),  # Room number
            ScrapSurface(function=self.__scrap_regex_value, title='Surface habitable'),  # Area
            ScrapMoreInfo(function=self.__scrap_kitchen, title="Type de cuisine"),  # Kitchen equipment
            ScrapMoreInfo(function=self.__scrap_furnished, title="Meublé"),  # Furnished
            ScrapMoreInfo(function=self.__scrap_open_fire, title='Feux ouverts', regex=r"(?P<number>\d)"),  # Open fire
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

        self.url = url
        self.data = []
        self.soup = None

    def get_data(self):

        if not self.data:
            self.run()

        return self.data

    def run(self):
        self.scrap()

    def scrap(self):

        # Fetch the page
        response = Request().get(self.url)
        self.soup = BeautifulSoup(response.content, "lxml")

        # Scrap the data
        for scrap in self.scrappers:
            result = scrap.function(scrap.tag, scrap.clasz, scrap.title, scrap.regex)

            # Store it
            self.data.append(result)

        self.data = list(flatten(self.data))

    def __scrap_locality(self, *args) -> Union[str, None]:

        title = self.__get_text(self.__scrap_field('h2', "section-title"))

        if title:
            regex = re.search(r"((\d){4} (?P<city>.+)$)", title.strip())

            if regex:
                return regex.group("city")

        return None

    def __scrap_garden_area(self, *args):
        return None

    def __scrap_terrace_area(self, *args):
        return None

    def __scrap_property_type(self, *args) -> list:
        house_type = house_subtype = None

        # Retrieve the property type field
        field = self.__get_text(self.__scrap_field_value("strong", "feature-label", "Type", "span"))

        if field:

            # Try to retrieve the type and subtype
            raw_subtype = re.search(r"^(?P<subtype>.+)\(.+\)$", field)
            raw_type = re.search(r"^.*\((?P<type>.+)\)$", field)

            if raw_subtype and raw_type:
                house_type = raw_type.group("type")
                house_subtype = raw_subtype.group("subtype")

            # If it fail, retrieve only the type:
            else:
                raw_type = re.search(r"^(?P<type>.+)$", field)

                # Return a list of the type, and None
                if raw_type:
                    house_type = raw_type.group("type")

        return [house_type, house_subtype]

    def __scrap_rooms_number(self, *args):
        # TODO: implement rooms number
        return 0

    """ SPECIAL METHODS --------------------------------------------
    The following methods are used only to scrap one specific thing.
    They can't be factored. They use Basics and Commons methods to
    work.
    """

    def __scrap_price(self, tag, attributes, *args) -> Union[str, None]:
        """Scrap the price."""

        # Retrieve the price field.
        field = self.__get_text(self.__scrap_field(tag, attributes))

        # If the field is not empty, retrieve the price
        if field:
            price = re.search(r"(?P<price>([0-9]{0,3}[.]?[0-9]{0,3}[.]?[0-9]{1,3})$)", tag.strip())

            if price:
                return price.group("price")

        return None

    def __scrap_sale_type(self, tag, attributes, *args) -> Union[str, None]:
        """Scrap the sale type."""

        # Retrieve the price field.
        sale = self.__scrap_field(tag, {"class": attributes})

        # Check if the price field contain a sale logo.
        if sale:
            icon = sale.find("svg")

            # If there's an icon, return "agence".
            if icon:
                return "agence"

            # If not, return "notariale"
            else:
                return "notariale"

        return None

    def __scrap_kitchen(self, tag, attributes, text, regex) -> bool:
        """Scrap if the house has a fully equiped kitchen or not."""

        # Check if there's a "Type de cuisine" field.
        if self.__scrap_regex_value(tag, attributes, text, regex):
            return True

        # If not, search in the description.
        return self.__scrap_description(r".*([Cc]uisine [Eée]quipée).*")

    def __scrap_furnished(self, tag, attributes, text, *args) -> bool:
        """Scrap if the house has furniture or not, by looking on the description."""

        # Check if there's a "" field.
        if self.__scrap_v_mark(tag, attributes, text):
            return True

        # If not, search in the description.
        return self.__scrap_description(r".*([mM]eublé|[mM]eubels).*")

    def __scrap_open_fire(self, tag, attributes, text, regex) -> bool:
        """Scrap if there's an open fire or not, by looking on the description."""

        # Check if there's a "Feu Ouverts" field.
        if self.__scrap_regex_value(tag, attributes, text, regex):
            return True

        # If not, search in the description.
        return self.__scrap_description(r".*([fF]eu [oO]uvert|[oO]pen [hH]aard).*")

    def __scrap_building_state(self, tag, attributes, *args) -> Union[str, None]:
        """Scrap the state of the building."""
        # TODO: Implement more guessing about if a house is old or to be renovated

        # The state can be found from two fields:
        fields = [
            ('Année de rénovation', "new"),
            ('Année de construction', 'old')
        ]

        # Loop through all field.
        for field in fields:
            result = self.__scrap_field_value(tag, attributes, field[0])

            # If a field exists, return the corresponding value.
            if result:
                return field[1]

        # Return None if nothing was scrapped.
        return None

    """ COMMON METHODS --------------------------------------------
    The following methods are reused to scrap multiple kind of
    data's. They use the Basic methods to work.
    """

    def __scrap_description(self, regex, *args) -> bool:
        """Scrap the description and look for match."""

        # Scrap the description.
        description = self.__get_text(self.__scrap_field('p', {"class": "description-block"}))

        # Find a match for the given regex.
        if description and re.match(regex, description, re.DOTALL):
            return True

        return False

    def __scrap_regex_value(self, tag, attributes, text, regex) -> Union[str, None]:
        """Scrap a value through a regex."""

        # Scrap the value's text
        result = self.__get_text(self.__scrap_field_value(tag, attributes, text))

        # If the text is not empty, apply regex.
        if result:
            regex = re.search(regex, result)

            # If the regex is not empty, return its value.
            if regex:
                return regex.group("number")

        # Return None if no value was found.
        return None

    def __scrap_v_mark(self, tag, attributes, text, *args) -> bool:
        """
        Scrap a value with a V mark.
        Used for: Swimming pool, garden.
        """

        # Scrap the value.
        result = self.__scrap_field_value(tag, attributes, text)

        # Check if there's a V mark in the field.
        if result and result.find('i', {"class": "zf-icon icon-check yes"}):
            return True

        # Return False if not.
        return False

    """ BASICS METHODS --------------------------------------------
    The following methods are the basic blocks used to create other
    scrapping functions.
    """

    def __scrap_field(self, tag, attributes, text=None) -> Union[Tag, None]:
        """Scrap a field and return it."""

        return self.soup.find(tag, {"class": attributes}, string=text)

    def __scrap_field_value(self, tag, attributes, text, next_tag='div') -> Union[Tag, bool]:
        """Scrap a field by its title and return the value of this field."""

        # Retrieve the field containing the given "text"
        title = self.__scrap_field(tag, attributes, text)

        # If it exists, return its value.
        if title:
            return title.find_next(next_tag)

        return False

    @staticmethod
    def __get_text(tag: Tag) -> Union[str, bool]:
        """Retrieve and return the text from a given BeautifulSoup Tag."""

        # If the tag is not empty, return its content.
        if tag:
            return tag.get_text()

        return False
