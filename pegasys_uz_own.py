import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from_drop_down = "//a[@class=\"selectBox ddrDepartureLocations selectBox-dropdown\"]"
bukhara_option = "//a[contains(text(),'Ташкент')]"
tashkent_option = "//a[contains(text(),'Ташкент')]"
search_btn = "//button[@id=\"search-button\"]"
result_table ="//table[@class=\"search-result-table\"]"


def get_element_by_data(data):
    element = "//option[contains(text(),'{}')]"
    element.format(data)
    return element


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

    def go_to_page(self, url):
        if not self.driver:
            raise RuntimeError("Driver not started. Call start_driver() first.")
        self.driver.get(url)

    def click_on(self, elem):
        wdw(self.driver, timeout=10).until(ec.visibility_of_element_located((By.XPATH, elem))).click()

    def perform_actions(self):
        self.click_on(from_drop_down)
        self.click_on(tashkent_option)
        self.click_on(search_btn)
        wdw(self.driver, timeout=10).until(ec.visibility_of_element_located((By.XPATH, result_table)))

    def parsing_data(self):
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'class': 'search-result-table'})
        current_url = self.driver.current_url
        data = []
        if table:
            rows = table.find_all('tr', class_='instant-confirmation tr-row')
            for row in rows:
                departure_date = row.find('td', class_='departure-date-column')
                package_name = row.find('div', class_='package-name')
                hotel_name = row.find('a')
                price_with_reduction = row.find('a', class_='button')
                if departure_date and package_name and hotel_name and price_with_reduction:
                    departure_date = departure_date.text.strip()
                    package_name = package_name.text.strip()
                    hotel_name = hotel_name.text.strip()
                    price_with_reduction = price_with_reduction.text.strip()
                data.append({
                    'departure_date': departure_date,
                    'package_name': package_name,
                    'hotel_name': hotel_name,
                    'price_with_reduction': price_with_reduction,
                    'booking_link': current_url if current_url else None,
                })
            # save_tour_data('Pegasys', data)
            for i in data:
                print(i)
        else:
            print("Table not found!")

    def parsing_data_from_html(self):
        pass


if __name__ == "__main__":
    url = 'https://pegasys.uz.pegast.asia'

    web_driver_handler = WebDriverHandler()
    # Running driver
    web_driver_handler.start_driver()

    try:
        web_driver_handler.go_to_page(url)
        web_driver_handler.perform_actions()
        web_driver_handler.parsing_data()
        # web_driver_handler.parsing_data_from_html()
    finally:
        web_driver_handler.stop_driver()
