
from src.cleaner.Saver import Saver
from threading import Thread
import pandas as pd


class Cleaner(Thread):

    default = pd.DataFrame(columns=[
        'locality',
        'type of property',
        'subtype of property',
        'price',
        'sale type',
        'number of rooms',
        'area',
        "kitchen equipment",
        "furnished",
        "open fire",
        "terrace",
        "terrace area",
        "garden",
        "garden area",
        "surface land",
        "surface plot land",
        "number of facades",
        "swimming pool",
        "building state"])

    def __init__(self, houses):
        """
        Receive the raw data from the Collector, clean/normalize it and
        save it.
        """
        super().__init__()

        self.houses = Cleaner.default

        # If house is not None
        if houses:

            # Append all entry to the dataset
            for house in houses:

                # Check if the entry is a list with a length of 19
                if house and type(house) == list and len(house) == 19:
                    self.houses.loc[len(self.houses)] = house

    def clean(self):
        self.__save()

    def __save(self):
        Saver(self.houses).save()

    @staticmethod
    def price_filter(x):
        ans = int(x.replace(".", ""))
        return ans

    @staticmethod
    def under_type_filter(x):
        return x.strip()

    @staticmethod
    def string_to_int(x : str):
        if x.isdecimal():
            return int(x)

        return None

    def cleaning(self, dataframe):
        pass





