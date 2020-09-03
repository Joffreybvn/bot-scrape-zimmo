
from threading import Thread


class Saver(Thread):

    def __init__(self, data):
        """
        Save the data into a CSV file.
        """

        super().__init__()
        self.data = data
