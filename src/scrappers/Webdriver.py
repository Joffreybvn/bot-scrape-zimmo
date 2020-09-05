
from selenium import webdriver

# https://helpfulsheep.com/2017-05-24-speeding-up-selenium/

# driver = "/Users/noahalvarezgonzalez/Drivers/chromedriver"
driver = "/usr/lib/chromium-browser/chromedriver"
options = webdriver.ChromeOptions()

# Block the ads
options.add_extension("./src/scrappers/extensions/ublock_origin_1_29_2_0.crx")

# Size to smallest possible
options.add_argument("window-size=1,1")

# Block the images and javascript
preferences = {
    "profile.managed_default_content_settings.javascript": 2,
    "profile.managed_default_content_settings.images": 2
}
options.add_experimental_option("prefs", preferences)


class WebDriver:

    def __init__(self):
        self.driver = webdriver.Chrome(driver, chrome_options=options)

    def get(self, url):
        return self.driver.get(url)

    def page_source(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()
