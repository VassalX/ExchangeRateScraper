from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread
import time
import sys
import json
import requests
import asyncio

server_url = sys.argv[1] if len(sys.argv) > 1  else 'http://localhost:8080/api/currency/'
url_currencies = 'https://markets.businessinsider.com/currencies'
chrome_driver_path = "./chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--headless')

def get_currencies():
    currencies = []
    wbdriver = webdriver.Chrome(executable_path = chrome_driver_path, options=chrome_options)
    with wbdriver as driver:
        wait = WebDriverWait(driver,10)
        driver.get(url_currencies)
        wait.until(presence_of_element_located((By.ID, "currency_container_table")))
        result = driver.find_element_by_id('currency_container_table')
        soup = BeautifulSoup(result.get_attribute('innerHTML'), 'html.parser')
        rows = soup.find_all('tr')
        for row in rows[2:]:
            tds = row.find_all('td')
            currency_name_short = tds[0].a.string.split("/")[1]
            country = tds[1].string.strip().replace('-','')
            currency_name = tds[2].a.string
            growth = float(tds[4].span.string.replace(',','').strip())
            price = float(tds[5].string.replace(',','').strip())
            timestamp = 0
            if not tds[6].find_all('span'):
                timestamp = datetime.strptime(tds[6].string.strip(), \
                    "%m/%d/%Y").timestamp()
            else:
                timestamp = datetime.strptime(tds[6].find_all('span')[1].string, \
                    "%m/%d/%Y %I:%M:%S %p UTC%z").timestamp()
            if not price or price == 0:
                continue
            currency = {
                "name": currency_name_short,
                "country": country,
                "fullName": currency_name,
                "growth": growth,
                "price": 1/price,
                "lastUpdateTimestamp": timestamp,
                "type": "cryptocurrency" if not country else "currency"
            }
            if not [x for x in currencies if x["name"]==currency_name_short or x["fullName"]==currency_name]:
                currencies.append(currency)
        print(len(currencies))
        return currencies

def send_cuurency():
    requests.post(server_url, json=get_currencies())

async def send_currencies_loop():
    while True:
        print(datetime.now().strftime("%H:%M:%S"))
        t = Thread(target=send_cuurency)
        t.daemon = True
        t.start()
        await asyncio.sleep(60)

if __name__ == '__main__':
    print(server_url)
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(send_currencies_loop())
        loop.run_forever()
    except:
        pass
    finally:
        print("Closing Loop")
        loop.close()