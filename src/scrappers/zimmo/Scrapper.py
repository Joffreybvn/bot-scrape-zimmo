
from src.scrappers.zimmo.Utils import Scrap, ScrapMoreInfo, ScrapSurface
from src.scrappers import WebDriver
from src.cleaner import Cleaner

import re
from threading import Thread
from typing import Union
from bs4 import BeautifulSoup, Tag
from pandas.core.common import flatten


class Scrapper(Thread):

    def __init__(self, urls):
        """
        Scrap all data from a given advertisement webpage and return it to
        the Manager.
        """
        super().__init__()

        self.scrappers = [
            Scrap(function=self.__scrap_locality, tag='h1', clasz='pand-title'),  # Locality
            Scrap(function=self.__scrap_property_type),  # Type and subtype of property
            Scrap(function=self.__scrap_price, tag='h1', clasz='pand-title'),  # Price
            Scrap(function=self.__scrap_sale_type, tag='div', clasz='price-box'),  # Sale type
            Scrap(function=self.__scrap_rooms_number),  # Room number
            ScrapSurface(function=self.__scrap_regex_value, title='Surface habitable'),  # Area
            ScrapMoreInfo(function=self.__scrap_kitchen, title="Type de cuisine"),  # Kitchen equipment
            ScrapMoreInfo(function=self.__scrap_furnished, title="Meublé"),  # Furnished
            ScrapMoreInfo(function=self.__scrap_open_fire, title='Feux ouverts', regex=r"(?P<number>\d)"),  # Open fire
            Scrap(function=self.__scrap_terrace_and_surface),
            ScrapMoreInfo(function=self.__scrap_v_mark, title='Jardin'),  # Garden
            # Garden Area (i = 11) - Calculated later
            ScrapSurface(function=self.__scrap_regex_value, title='Surface construite'),  # Surface of the land
            ScrapSurface(function=self.__scrap_regex_value, title='Superficie du terrain'),  # Plot of land
            ScrapMoreInfo(function=self.__scrap_regex_value, title='Construction', regex=r"(?P<number>\d)-façades"),  # Facades
            ScrapMoreInfo(function=self.__scrap_v_mark, title='Terrasse'),  # Swimming Pool
            ScrapMoreInfo(function=self.__scrap_building_state)  # Building
        ]

        self.driver = WebDriver()
        self.data = []
        self.soup = None
        self.urls = urls

    def get_data(self):

        if not self.data:
            self.run()

        return self.data

    def run(self):
        self.scrap_all()

    def scrap_all(self):

        for url in self.urls:
            self.scrap(url)

        self.driver.close()

    def scrap(self, url):

        if self.driver.get(url) is not None:
            self.soup = BeautifulSoup(self.driver.page_source(), "lxml")
            house = []

            # Scrap the data
            for scrap in self.scrappers:
                result = scrap.function(scrap.tag, scrap.clasz, scrap.title, scrap.regex)

                # Store it
                house.append(result)

            # Math the garden area, and insert it to the list
            garden_area = self.__math_garden_area(house[12], house[11])
            house.insert(12, garden_area)

            self.data.append(list(flatten(house)))

    @staticmethod
    def __math_garden_area(plot_surface, build_surface):

        # If plot_surface and build_surface are not None:
        if plot_surface and build_surface:

            # Convert string to int
            plot_surface = Cleaner.string_to_int(plot_surface.strip())
            build_surface = Cleaner.string_to_int(build_surface.strip())

            # If plot_surface and build_surface exists:
            if plot_surface and build_surface:
                print(plot_surface - build_surface)
                return plot_surface - build_surface

        return None

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
            #price = re.search(r"(?P<price>([0-9]{0,3}[.]?[0-9]{0,3}[.]?[0-9]{1,3})$)", field.strip())
            price = re.search(r".*€ (?P<price>[0-9.]+)", field)

            if price:
                return price.group("price")
        return None

    def __scrap_sale_type(self, tag, attributes, *args) -> Union[str, None]:
        """Scrap the sale type."""

        # Retrieve the price field.
        sale = self.__scrap_field(tag, attributes)

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

    def __scrap_property_type(self, *args) -> list:
        """
        Scrap the property type and subtype. Return a tuple with type
        and subtype.
        """

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

    def __scrap_terrace_and_surface(self, *args):
        """
        Scrap the terrace and its surface. Return a tuple of terrace
        and surface.
        """
        terrace = surface = None

        # Search for the surface area in "col-xsm-8 col-sm-3 info-name"
        raw_surface = self.__scrap_regex_value("div", "col-xsm-8 col-sm-3 info-name", "Terrasse", r"(?P<number>\d*) m²")

        # If there's an area, set Terrace to true and save the seurface
        if raw_surface:
            terrace = True
            surface = raw_surface

        # If not, search if there's a terrace in the "col-xs-7 info-name" field
        else:
            v_mark = self.__scrap_v_mark("div", "col-xs-7 info-name", "Terrasse")
            text = self.__get_text(self.__scrap_field_value("div", "col-xs-7 info-name", "Jardin"))

            # If there's a V-mark in "Terrasse" or the "Terrasse" word in "Jardin":
            if v_mark or (text and "Terrasse" in text):
                terrace = True

        return [terrace, surface]

    def __scrap_locality(self, tag, attributes, *args) -> Union[str, None]:
        """Scrap the locality from the advertisement title."""

        # Retrieve the title
        title = self.__get_text(self.__scrap_field(tag, attributes))

        # Regex the locality
        if title:
            regex = re.search(r".*à (?P<locality>.*) pour .*", title, re.DOTALL)

            # If a locality is found, return it
            if regex:
                return regex.group("locality")

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
        description = self.__get_text(self.__scrap_field('p', "description-block"))

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
