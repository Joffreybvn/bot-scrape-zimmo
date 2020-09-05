
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

        self.data = []
        self.to_clean = houses

    def clean(self):
        self.data = Cleaner.default.copy()

        # If house is not None
        if self.to_clean:

            # Append all entry to the dataset
            for entry in self.to_clean:

                # Check if the entry is a list with a length of 19
                if entry and type(entry) == list and len(entry) == 19:
                    self.data.loc[len(self.data)] = entry
        self.__save()

    def __save(self):
        print("to save")
        print(self.data)
        Saver(self.data).save()

    @staticmethod
    def price_filter(x):
        ans = int(x.replace(".", ""))
        return ans

    @staticmethod
    def under_type_filter(x):
        return x.strip()

    @staticmethod
    def string_to_int(x: str):
        if x.isdecimal():
            return int(x)

        return None

    def cleaning(self, dataframe):
        pass






