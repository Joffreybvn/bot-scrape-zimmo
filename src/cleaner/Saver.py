
from threading import Thread
from random import sample
from string import digits


class Saver(Thread):

    path = "./backup/"

    def __init__(self, dataframe):
        """
        Save the data into a Pickle file.
        """

        super().__init__()
        self.dataframe = dataframe

    def save(self):

        filename = "".join(sample(digits, 10))
        self.dataframe.to_pickle(f"{Saver.path}{filename}.p", compression='infer', protocol=4)
