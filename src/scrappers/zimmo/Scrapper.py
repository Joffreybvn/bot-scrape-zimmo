
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

attributes = [

        {   # 0 - default : num_rooms, kitchen_equipment, furnished,
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
                "text":"Construction"
            },
            "sanitizer": "facade"
        },
        {  # 2 - state_building
           # is in //div @class="col-xs-7 info-name"
            "tag": 'div',
            "attributes": {
                "class": "col-xs-7 info-name",
                "text":"Année de rénovation"
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

class Scrapper(Thread):

    def __init__(self, url):
        """
        Scrap all data from a given advertisement webpage and return it to
        the Manager.
        """

        super().__init__()
        self.url = url

    # Exclure viager & tout sauf maison/appartement

    def __scrap_locality(self):
        pass

    def __scrap_property_type(self):
        pass

    def __scrap_property_subtype(self):
        pass

    def __scrap_price(self):
        pass

    def __scrap_sale_type(self):
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
        pass

    def __scrap_swimming_pool(self):
        pass

    def __scrap_building_state(self):
        pass
