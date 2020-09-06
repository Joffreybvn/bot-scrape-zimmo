
from threading import Thread
from random import sample
from string import digits


class Saver(Thread):

    path = "./backup/"

    def __init__(self, dataframe):
        """
        Save a given dataframe into a randomly named Pickle file.

        :param dataframe: A pandas Dataframe containing real estate data.
        """

        super().__init__()
        self.dataframe = dataframe

    def save(self):
        """Save the self.dataframe into a Pickle file."""

        # Randomize the name.
        filename = "".join(sample(digits, 10))

        # Save the file in "./backup/".
        self.dataframe.to_pickle(f"{Saver.path}{filename}.p", compression='infer', protocol=4)
