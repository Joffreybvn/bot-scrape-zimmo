
from typing import Union
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

    def __init__(self, raw_data):
        """
        Receive the raw data from the Collector, clean/normalize it and
        save it.
        """
        super().__init__()

        self.df = Cleaner.default.copy()
        self.to_clean = raw_data

    def clean(self):

        # Append the data given to this class to the dataframe
        self.append_data()

        # Clean the price
        self.df['price'] = self.df['price'].apply(lambda x: self.__clean_price(x))

        # Clean the property subtype
        self.df['subtype of property'] = self.df['subtype of property'].apply(lambda x: self.__clean_subtype(x))

        self.__save()

    def append_data(self):
        """Append the data to clean to the dataframe."""

        # If the data to clean is not empty
        if self.to_clean:

            # Append all entry to the dataset
            for entry in self.to_clean:

                # Check if the entry is a list with a length of 19
                if entry and type(entry) == list and len(entry) == 19:
                    self.df.loc[len(self.df)] = entry

    def __save(self):
        Saver(self.df).save()

    def __clean_price(self, price: str) -> Union[int, None]:
        if price:
            return self.string_to_int(price.replace(".", ""))

        return None

    def __clean_subtype(self, subtype) -> Union[str, None]:
        if subtype:
            return self.__sanitize_string(subtype)

        return None

    @staticmethod
    def __sanitize_string(string: str) -> str:
        return string.strip()

    @staticmethod
    def string_to_int(x: str) -> Union[int, None]:

        if x.isdecimal():
            return int(x)

        return None
