
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
        for file in glob.glob(f"{Saver.real_estate_data}*.p"):

            pickle = pd.read_pickle(file)
            self.df = pd.concat([self.df, pickle])

        # TODO: Transcrire les Booléens en 0 ou 1
        # Replace None to "None" (string) in the CSV
        self.df[["swimming pool", "garden"]] = self.df[['swimming pool', "garden"]].apply(lambda x: self.true_to_1(x))
        self.df.fillna("None", inplace=True)

        self.df.to_csv("result.csv")

    @staticmethod
    def true_to_1(x):
        if x == True:
            return 1
        elif x == False:
            return 0
        return None


