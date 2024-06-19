from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchDriverException, WebDriverException


class WebHumoTourHandler:
    def __init__(self, headless: bool = False):
        chrome_option = Options()
        chrome_option.add_argument('--no-sandbox')
        if headless:
            chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_option)

    def load_page(self, url: str):
        try:
            self.driver.get(url)
            print(f"Page loaded successfully: {url}")
        except TimeoutException:
            print("Timeout waiting for page to load.")
        return True

    def driver_quit(self):
        self.driver.quit()


def main():
    url1: str = "http://humotouroperator.uz/search_tour"
    web_driver_handler: WebHumoTourHandler = WebHumoTourHandler(True)
    web_driver_handler.load_page(url1)
    web_driver_handler.driver_quit()


if __name__ == '__main__':
    main()
