import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url: str = "https://medicalka.com"

chrome_option = Options()
# chrome_option.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_option)
driver.get(url)
time.sleep(10)
driver.quit()


