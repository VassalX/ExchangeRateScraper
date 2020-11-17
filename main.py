import requests
from bs4 import BeautifulSoup

URL = 'https://www.exchangerates.org.uk/US-Dollar-USD-currency-table.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find('div', class_='css-panes')
col1 = tables.find_all('tr', class_='colone')
col2 = tables.find_all('tr', class_='coltwo')
cols = col1 + col2
results = []
for col in cols:
    tds = col.find_all('td')
    flag = tds[2].span['class'][1]
    currency = tds[3].a.string
    value_of_one = tds[4].b.string
    short_currency = tds[5].a.string.split(" ")[1]
    value_in_one = tds[7].b.string
    results.append({
        "flag": flag,
        "currency_name": currency,
        "value_of_one": value_of_one,
        "currency_name_short": short_currency,
        "value_in_one": value_in_one
    })
print(*results, sep='\n')