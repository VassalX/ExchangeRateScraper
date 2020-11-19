from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys

url = 'https://markets.businessinsider.com/currencies'
chrome_driver_path = "./chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--headless')

def get_currencies():
    currencies = []
    wbdriver = webdriver.Chrome(executable_path = chrome_driver_path, options=chrome_options)
    with wbdriver as driver:
        wait = WebDriverWait(driver,10)
        driver.get(url)
        wait.until(presence_of_element_located((By.ID, "currency_container")))
        result = driver.find_element_by_id('currency_container')
        soup = BeautifulSoup(result.get_attribute('innerHTML'), 'html.parser')
        rows = soup.find_all('tr')
        for row in rows[2:]:
            tds = row.find_all('td')
            currency_name_short = tds[0].a.string.split("/")[1]
            country = tds[1].string.strip()
            currency_name = tds[2].a.string
            if not country or country == '-':
                continue
            growth = float(tds[4].span.string)
            price = float(tds[5].string.replace(',','').strip())
            times_str = tds[6].find_all('span')[1].string
            timestamp = get_timestamp(times_str)
            currency = {
                "currency_name_short": currency_name_short,
                "country": country,
                "currency_name": currency_name,
                "growth": growth,
                "price": price,
                "timestamp": timestamp
            }
            currencies.append(currency)
        driver.close()
        return currencies

def get_timestamp(times_str):
    return datetime.strptime(times_str, "%m/%d/%Y %I:%M:%S %p UTC%z").timestamp()

# print(datetime.fromtimestamp(get_timestamp('11/18/2020 05:16:00 PM UTC-0500')).strftime("%d/%m/%y %H:%M:%S %z"))
print(*get_currencies(),sep='\n')