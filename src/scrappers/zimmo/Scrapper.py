
from threading import Thread


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
