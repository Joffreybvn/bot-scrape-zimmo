
import glob
import pandas as pd


class Merger:

    path = "./backup/"

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

    def __init__(self):
        """
        Merge pickle files into one CSV.
        """
        self.houses = Merger.default

    def merge(self):

        # Retrieve all pickles
        for file in glob.glob(f"{Merger.path}*.p"):

            pickle = pd.read_pickle(file)
            print(pickle)
            self.houses = pd.concat([self.houses, pickle])

        # print a CSV
        self.houses.fillna("None", inplace=True)
        self.houses.to_csv("result.csv")

