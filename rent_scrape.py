import requests
import re
from bs4 import BeautifulSoup
import pandas

begin = 'https://www.aruodas.lt/butu-nuoma/vilniuje/puslapis/'
end = '?FPriceMin=200&FPriceMax=300&detailed_search=1&FAddDate=1'

r = requests.get(begin + '1' + end)
c = r.content

soup = BeautifulSoup(c, "html.parser")

page_nr = soup.find_all("a", {"class": "page-bt"})[-2].text

list_ = []

for page in range(1, int(page_nr)):
    r = requests.get(begin + str(page) + end)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("tr", {"class": "list-row"})

    for item in all:
        d = {}
        if len(item.find_all('div', {'class': 'lazybanner'})) > 0:
            pass
        else:

            try:
                d['page'] = item.find_all(
                    'td', {'class': 'list-adress'})[0].find_all('a', href=True)[0]['href']
            except:
                d['page'] = None

            try:
                d['address'] = item.find_all(
                    'td', {'class': 'list-adress'})[0].find_all('a')[0].text
            except:
                d['address'] = None
            try:
                d['date'] = item.find_all(
                    'p', {'class': 'flat-rent-dateadd'})[0].text
            except:
                d['date'] = None
            try:
                d['price'] = item.find_all(
                    'span', {'class': 'list-item-price'})[0].text
            except:
                d['price'] = None
            try:
                d['rooms'] = item.find_all(
                    'td', {'class': 'list-RoomNum'})[0].text.replace(' ', '').replace('\n', '')
            except:
                d['rooms'] = None
            try:
                d['area'] = item.find_all(
                    'td', {'class': 'list-AreaOverall'})[0].text.replace(' ', '').replace('\n', '')
            except:
                d['area'] = None
            try:
                d['floor'] = item.find_all(
                    'td', {'class': 'list-Floors'})[0].text.replace(' ', '').replace('\n', '')
            except:
                d['floor'] = None
            list_.append(d)


def click(link):
    return '<a target="_blank" href="{}">{}</a>'.format(link, 'aruodas')


df = pandas.DataFrame(list_)
df = df[['date', 'price', 'address', 'rooms', 'area', 'floor', 'page']]
df = df.sort_values(by=['price', 'date'])
#df.to_csv("rent.csv")
df = df.style.format({'page': click})

df

