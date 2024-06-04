import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# XPATHS
x_elem = "//div[@id=\"samo_popup\"]/div/div[1]"
from_drop_menu = "//div[@class=\"chosen-container chosen-container-single TOWNFROMINC_chosen\"]"
tashkent_option = "//li[contains(text(), 'Ташкент ')]"
to_option_drop_menu: str = "//select[@name=\"STATEINC\"]"
to_options = '//li[contains(text(), "{}")]'
to_options.format("Вьетнам")
search_btn = "//button[@class=\"load right\"]"


class WebDriverHandler:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def wait_for_element(self, by, value, timeout=10):
        return wdw(self.driver, timeout).until(ec.visibility_of_element_located((by, value)))

    def click_on(self, elem):
        return wdw(self.driver, timeout=20).until(ec.visibility_of_element_located((By.XPATH, elem))).click()

    def go_to_page(self, url):
        if not self.driver:
            raise RuntimeError("Driver not started. Call start_driver() first.")
        self.driver.get(url)

    def perform_actions(self):
        self.click_on(x_elem)
        self.click_on(from_drop_menu)
        self.click_on(tashkent_option)

        print("Passed")


if __name__ == "__main__":
    url = "https://online.kompastour.uz/search_tour"

    web_driver_handler = WebDriverHandler()
    web_driver_handler.start_driver()

    try:
        web_driver_handler.go_to_page(url)
        web_driver_handler.perform_actions()
    finally:
        web_driver_handler.stop_driver()
