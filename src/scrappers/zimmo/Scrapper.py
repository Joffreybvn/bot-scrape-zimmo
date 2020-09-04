
from threading import Thread

from bs4 import BeautifulSoup
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
        self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.url = url
        self.data = []


    def get_data(self):
        return self.data

    def scrap(self):

        #Fetch the page
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "lxml")

        self.__scrap_price(soup, 'div', 'price-box')
        self.__scrap_furnished(soup)
        self.__scrap_open_fire(soup)
        self.__scrap_terrace(soup, 'div', 'col-xs-7 info-name', 'Terrasse')
        self.__scrap_garden(soup, 'div', 'col-xs-7 info-name', 'Jardin')
        self.__scrap_house_surface(soup, 'div', 'col-xs-7 info-name', 'Surf. habitable')
        self.__scrap_plot_surface(soup, 'div', 'col-xs-7 info-name', 'Sup. du terrain')
        self.__scrap_facades(soup, 'div', 'col-xs-7 info-name', 'Construction')
        self.__scrap_swimming_pool(soup, 'div', 'col-xs-7 info-name', 'Piscine')
        self.__scrap_building_state(soup, 'div', 'col-xs-7 info-name', 'Année de rénovation')

        self.driver.close()


    def retrieve_content(self, tag, attributes=None):

        if attributes is None:
            attributes = {}

        return self.source.find_all(tag, attrs=attributes)

    def retrieve_all_raw_content(self):

        # Loop through the attributes and retrieve each corresponding element
        for entry in Scrapper.attributes:
            self.data.append(
                self.sanitize(entry['sanitizer'], self.retrieve_content(entry['tag'], entry['attributes'])[0]))


    def __scrap_locality(self, tag, attributes):
        for elem in soup.find_all(tag, attributes):
            m = re.search(r"((\d){4} (?P<city>.+)$)", elem.text.strip())
            return m.group("city"))

        pass

    def __scrap_property_type(self):
        pass

    def __scrap_property_subtype(self):
        pass

    def __scrap_price(self, tag, attributes):
        for elem in soup.find_all(tag, attributes):
            n = re.search(r"(?P<price>([0-9]{0,3}[.]?[0-9]{0,3}[.]?[0-9]{1,3})$)", elem.text.strip())
            print(n.group("price"))

        pass

    def __scrap_sale_type(self):
        for elem in soup.find_all('div', attrs={"class": "price-box"}):
            o = elem.find_all("svg")
            print(o)
            if not o:
                print('vente notariale')
            else:
                print('vente par agence')
        pass

    def __scrap_rooms_number(self):
        pass

    def __scrap_area(self):
        pass

    def __scrap_kitchen(self):
        pass

    def __scrap_furnished(self, soup):
        if ("meublé" or "meubels") in soup.lower():
            print("yes")
        else:
            print("no")

    def __scrap_open_fire(self, soup):
        if ("feu ouvert" or "open haard") in soup.lower():
            print("yes")
        else:
            print("no")

    def __scrap_terrace(self, soup, tag, attributes, text):
        result = self.__scrap_title_field(soup, tag, attributes, text)
        if result.find('i', {"class": "zf-icon icon-check yes"}):
            return True
        else:
            return False

    def __scrap_garden(self, soup, tag, attributes, text):
        result = self.__scrap_title_field(soup, tag, attributes, text)
        if result.find('i', {"class": "zf-icon icon-check yes"}):
            return True
        else:
            return False

    def __scrap_house_surface(self, soup, tag, attributes, text):
        return self.__scrap_title_field(self, soup, tag, attributes, text).get_text()

    def __scrap_plot_surface(self, soup, tag, attributes, text):
        return self.__scrap_title_field(self, soup, tag, attributes, text).get_text()

    def __scrap_facades(self, soup, tag, attributes, text):
        facades = self.__scrap_title_field(self, soup, tag, attributes, text).get_text()
        result = re.search(r"(?P<amount>\d)-façades", facades)
        return result.group("amount")

    def __scrap_swimming_pool(self, soup, tag, attributes, text):
        result = self.__scrap_title_field(soup, tag, attributes, text)
        if result.find('i', {"class": "zf-icon icon-check yes"}):
            return True
        else:
            return False

    def __scrap_building_state(self, soup, tag, attributes, text):
        return self.__scrap_title_field(soup, tag, attributes, text).get_text()

    def __scrap_title_field(self, soup, tag, attributes, text):
        return soup.find(tag, attributes, string=text).find_next('div')