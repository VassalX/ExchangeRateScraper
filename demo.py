from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
import time
import sys

url = 'https://markets.businessinsider.com/currencies'
chrome_driver_path = "./chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(
    executable_path = chrome_driver_path, options=chrome_options
)

with webdriver as driver:
    wait = WebDriverWait(driver,10)
    driver.get(url)
    wait.until(presence_of_element_located((By.ID, "currency_container")))
    results = driver.find_element_by_id('currency_container')
    print(results)

    
