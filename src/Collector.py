
import concurrent
from concurrent.futures import wait
from concurrent.futures import ThreadPoolExecutor
from src.scrappers.zimmo import Manager


class Collector:

    def __init__(self):
        """
        Collect the raw data from the Manager and save it into CSV
        files through the Cleaner.
        """

    def start(self):

        manager = Manager()
        manager.start()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(Manager.scrapper, url) for url in manager.urls]

            for entry in concurrent.futures.as_completed(futures):
                print(entry.result())
