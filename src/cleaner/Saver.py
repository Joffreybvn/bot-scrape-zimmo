
from threading import Thread
import pickel
import pandas as pd


class Saver(Thread):

    def __init__(self, data):
        """
        Save the data into a CSV file.
        """

        super().__init__()
        self.data = data

    def to_pickel (self, data):
        for i in len (num_threading):
            self.data.to_pickel(f"./pickel_chunk{i}.pkl")

    def merge_pickel (self):
