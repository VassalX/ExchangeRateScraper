import requests
from bs4 import BeautifulSoup

URL = 'https://www.exchangerates.org.uk/US-Dollar-USD-currency-table.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('div', class_='css-panes')
row1 = table.find_all('tr', class_='colone')
row2 = table.find_all('tr', class_='coltwo')
rows = row1 + row2
results = []
for row in rows:
    tds = row.find_all('td')
    flag = tds[2].span['class'][1]
    currency_name = tds[3].a.string
    value_of_one = float(tds[4].b.string)
    currency_name_short = tds[5].a.string.split(" ")[1]
    value_in_one = float(tds[7].b.string)
    if value_of_one and value_in_one:
        results.append({
            "flag": flag,
            "currency_name": currency_name,
            "value_of_one": value_of_one,
            "currency_name_short": currency_name_short,
            "value_in_one": value_in_one
        })

print(*results, sep='\n')

# URL = 'https://www.x-rates.com/table/?from=USD&amount=1'
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup)
# table_cont = soup.find(id="currency_container")
# print(table_cont)
# table = table_cont.find("table")
# rows = table.find_all("tr", class_="row-hover")
# results = []
# for row in rows:
#     tds = row.find_all('td')
#     currency_name_short = tds[0].a.string.split("/")[1]
#     country = tds[1].string
#     currency_name = tds[2].a.string
#     change = tds[4].span.string
#     price = tds[5].string
#     time = tds[6].span.string
#     value = {
#         "currency_name_short": currency_name_short,
#         "country": country,
#         "currency_name": currency_name,
#         "change": change,
#         "price": price,
#         "time": time
#     }
#     results.append(value)

# print(*results, sep="\n")