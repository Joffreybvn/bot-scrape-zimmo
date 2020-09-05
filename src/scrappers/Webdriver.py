
from random import choice
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


#driver = "/Users/noahalvarezgonzalez/Drivers/chromedriver"
driver = "/usr/lib/chromium-browser/chromedriver"
options = webdriver.ChromeOptions()

# Block the ads
# options.add_extension("./src/scrappers/extensions/ublock_origin_1_29_2_0.crx")

# Size to smallest possible
#options.add_argument("window-size=1,1")

# Block the images and javascript
preferences = {
    # "profile.managed_default_content_settings.javascript": 2,
    # "profile.managed_default_content_settings.images": 2
}
options.add_experimental_option("prefs", preferences)

# Add a proxy
PROXIES = [
    "176.31.141.21:51327",
    "51.77.163.186:8080",
    "91.121.33.63:1000",
    "176.31.141.20:51327",
    "54.38.110.35:48034",
    "51.254.182.54:1000",
    "159.8.114.37:80",
    "151.80.201.162:1080",
    "51.68.61.17:5000"
]

proxy = Proxy()
proxy.proxyType = ProxyType.MANUAL
proxy.autodetect = False


class WebDriver:

    def __init__(self):

        # Load a random proxy
        self.proxy = choice(PROXIES)
        proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = self.proxy
        options.Proxy = proxy
        options.add_argument("ignore-certificate-errors")

        self.driver = webdriver.Chrome(driver, chrome_options=options)
        self.driver.implicitly_wait(30)
        # self.driver.set_window_size(1, 1)

    def get(self, url):
        if url:
            self.driver.get(url)

            # Wait for the page to load
            try:
                self.driver.find_element_by_xpath("//*[@data-ga='Feedback,click,Side button']")
            except:
                print[f"[x] Failed to load the page. Maybe the website is blocking us ? - {url}"]
            else:
                return True

        return None

    def page_source(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()
