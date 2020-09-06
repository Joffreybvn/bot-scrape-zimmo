
from src.cleaner.Cleaner import Cleaner
from src.cleaner.Saver import Saver

import glob
import pandas as pd


class Merger:

    def __init__(self):
        """
        Merge pickle files into one CSV.
        """
        self.df = Cleaner.default.copy()

    def merge(self):

        # Retrieve all pickles
        for file in glob.glob(f"{Saver.path}*.p"):

            pickle = pd.read_pickle(file)
            self.df = pd.concat([self.df, pickle])

        # TODO: Transcrire les Booléens en 0 ou 1
        # Replace None to "None" (string) in the CSV
        self.df.fillna("None", inplace=True)

        self.df.to_csv("result.csv")
