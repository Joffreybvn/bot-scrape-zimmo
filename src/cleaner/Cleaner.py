
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
