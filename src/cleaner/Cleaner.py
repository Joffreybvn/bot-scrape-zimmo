
from src.cleaner import Saver
from threading import Thread


class Cleaner(Thread):

    def __init__(self, raw):
        """
        Receive the raw data from the Collector, clean/normalize it and
        save it.
        """

        super().__init__()
        self.raw = raw

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





