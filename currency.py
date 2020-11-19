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
import json
import requests

url_currencies = 'https://markets.businessinsider.com/currencies'
url_crypto_currencies = 'https://markets.businessinsider.com/cryptocurrencies'
chrome_driver_path = "./chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--headless')

def get_currencies():
    currencies = []
    wbdriver = webdriver.Chrome(executable_path = chrome_driver_path, options=chrome_options)
    with wbdriver as driver:
        wait = WebDriverWait(driver,10)
        driver.get(url_currencies)
        wait.until(presence_of_element_located((By.ID, "currency_container")))
        result = driver.find_element_by_id('currency_container')
        soup = BeautifulSoup(result.get_attribute('innerHTML'), 'html.parser')
        rows = soup.find_all('tr')
        for row in rows[2:]:
            tds = row.find_all('td')
            currency_name_short = tds[0].a.string.split("/")[1]
            country = tds[1].string.strip().replace('-','')
            currency_name = tds[2].a.string
            growth = float(tds[4].span.string)
            price = float(tds[5].string.replace(',','').strip())
            timestamp = 0
            if not tds[6].find_all('span'):
                timestamp = datetime.strptime(tds[6].string.strip(), \
                    "%m/%d/%Y").timestamp()
            else:
                timestamp = datetime.strptime(tds[6].find_all('span')[1].string, \
                    "%m/%d/%Y %I:%M:%S %p UTC%z").timestamp()
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
        return json.dumps(currencies)

currs = get_currencies()
response = requests.post('http://localhost:5000/', json=currs)
print(*response.json(), sep="\n")