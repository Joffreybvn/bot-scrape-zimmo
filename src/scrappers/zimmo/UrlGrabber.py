
from threading import Thread


class UrlGrabber(Thread):

    def __init__(self, province):
        """
        Scrap the urls of all advertisement's webpage and return it to
        the Manager.
        """

        super().__init__()
        self.province = province
