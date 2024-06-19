import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec

database = []
# CSSs
from_input_field_css = "#departure-location > a"
to_input_field_css = "#destination-country > a"
to_drop_down_options = "body > ul.selectBox-dropdown-menu.selectBox-options.selectBox-selectBox-dropdown-menu.ddrDestinationCountries-selectBox-dropdown-menu > li > a"
search_btn_css = "#search-button"
def get_index_num():
    print("Ketadigan shaharni tanlang:")
    cities = {"Бухара": "2", "Наманган": "3", "Самарканд": "4", "Ташкент": "5", "Фергана": "6"}
    print("Shaharni tanlang:")
    for e in cities:
        print(f"--{e} uchun {cities[e]}")
    i: int = int(input(f":>>>"))
    return i


def print_database():
    for i in database:
        print(i)


class WebDriverHandler:

    def __init__(self):
        self.driver = None

    def setup_driver(self, url):
        chrome_option = Options()
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-dev-5shm-usage')
        self.driver = webdriver.Chrome(options=chrome_option)
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def click_on_by_css(self, css_elem: str):
        return wdw(self.driver, timeout=10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, css_elem))).click()

    def set_from_input_field(self, num: int):
        self.click_on_by_css(from_input_field_css)
        option_by_num_css = f"body > ul.selectBox-dropdown-menu.selectBox-options.selectBox-selectBox-dropdown-menu.ddrDepartureLocations-selectBox-dropdown-menu > li:nth-child({num}) > a"
        self.click_on_by_css(option_by_num_css)

    def set_to_input_field(self):
        to_option_list = []
        self.click_on_by_css(to_input_field_css)
        options = self.driver.find_elements(By.CSS_SELECTOR, to_drop_down_options)
        for e in options:
            elem = e.get_attribute("rel")
            to_option_list.append(elem)
        return to_option_list

    def perform_actions(self, num):
        self.driver.refresh()
        self.set_from_input_field(num)
        o_list = len(self.set_to_input_field())
        print(o_list)
        for n in range(o_list):
            n = str(n+1)
            options_css = f"body > ul.selectBox-dropdown-menu.selectBox-options.selectBox-selectBox-dropdown-menu.ddrDestinationCountries-selectBox-dropdown-menu > li:nth-child({n}) > a"
            print(options_css)
            print(n)
            self.click_on_by_css(to_input_field_css)
            self.driver.find_element(By.CSS_SELECTOR, options_css)
            time.sleep(2)
            self.click_on_by_css(search_btn_css)
            time.sleep(5)
            self.update_database()

    def update_database(self):
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'class': 'search-result-table'})
        current_url = self.driver.current_url
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
                database.append({
                    'departure_date': departure_date,
                    'package_name': package_name,
                    'hotel_name': hotel_name,
                    'price_with_reduction': price_with_reduction,
                    'booking_link': current_url if current_url else None,
                })
            # save_tour_data('Pegasys', data)
        else:
            print("Table not found!")


if __name__ == "__main__":
    m = get_index_num()
    url1 = "https://pegasys.uz.pegast.asia"
    web_driver_handler = WebDriverHandler()
    web_driver_handler.setup_driver(url1)
    web_driver_handler.perform_actions(m)
    web_driver_handler.stop_driver()
    print_database()
