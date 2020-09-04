
from threading import Thread

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
        self.url = url
        self.data = []


    # Exclure viager & tout sauf maison/appartement

    def init_driver():
        driver = copy.copy(webdriver)
        driver.implicitly_wait(30)

        return driver

    def get_data(self):
        return self.data



    def Scrap(self):

        #Fetch the page
        self.driver.get(self.url)

        #Save the source of the page
        time.sleep(1)
        self.source = BeautifulSoup(self.driver.page_source, 'lxml')
        self.driver.close()

        #Lauch scrappers and retrieve content

    def retrieve_content(self, tag, attributes=None):

        if attributes is None:
            attributes = {}

        return self.source.find_all(tag, attrs=attributes)

    def retrieve_all_raw_content(self):

        # Loop through the attributes and retrieve each corresponding element
        for entry in Scrapper.attributes:
            self.data.append(
                self.sanitize(entry['sanitizer'], self.retrieve_content(entry['tag'], entry['attributes'])[0]))


    def __scrap_locality(self):
        for elem in self.source.find_all(tag, attrs=attributes):
            m = re.search(r"((\d){4} (?P<city>.+)$)", elem.text.strip())
            return m.group("city"))

        pass

    def __scrap_property_type(self):
        pass

    def __scrap_property_subtype(self):
        pass

    def __scrap_price(self, sanitizer):
        for sanitizer == "price"
        for elem in self.source.find_all(tag, attrs=attributes):
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

    def __scrap_furnished(self):
        pass

    def __scrap_open_fire(self):
        driver.get(url)
        text = driver.page_source
        if ("feu ouvert" or "open haard") in text.lower():
            print("yes")
        else:
            print("no")

        pass

    def __scrap_terrace(self):
        pass

    def __scrap_garden(self):
        pass

    def __scrap_house_surface(self):
        pass

    def __scrap_plot_surface(self):
        pass

    def __scrap_facades(self):
        def find_facades(url, tag, attributes, text):
            # Retrieve the page and parse it to bs4
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            driver.close()

            # Retrieve the content
            facades = soup.find(tag, attributes, string=text).find_next('div').get_text()
            result = re.search(r"(?P<amount>\d)-façades", facades)
            return result.group("amount")

        pass

    def __scrap_swimming_pool(self):
        def find_pool(url, tag, attributes, text):

            # Retrieve the page and parse it to bs4
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            driver.close()

            # Retrieve the content
            result = soup.find(tag, attributes, string=text).find_next('div')

            if result.find('i', {"class": "zf-icon icon-check yes"}):
                return True
            else:
                return False

        pass

    def __scrap_building_state(self):
        def find_entry(url, tag, attributes, text):
            # Retrieve the page and parse it to bs4
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            driver.close()

            # Retrieve the content
            return soup.find(tag, attributes, string=text).find_next('div').get_text()

        pass
