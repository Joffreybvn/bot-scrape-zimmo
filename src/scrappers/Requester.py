
import requests


# https://www.xml-sitemaps.com/
class Requester:

    options = {
        'Accept': '*/*',
        'Host': 'www.zimmo.be',
        'User-Agent': 'Mozilla/5.0 (compatible; XML Sitemaps Generator; www.xml-sitemaps.com) Gecko XML-Sitemaps/1.0'
    }

    def __init__(self):
        pass

    @staticmethod
    def get(url):
        return requests.get(url, headers=Requester.options)
