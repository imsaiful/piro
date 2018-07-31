import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime, timedelta


url = 'https://www.ndtv.com'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
# strhtm = soup.prettify()
# d=soup.find(class_='itg-listing')
# Print the first few characters
i = 1
data = ""
da = []
d1 = []
href = []
date = []
d = datetime.now() - timedelta(1)
for x in soup.find_all('a'):

    try:
        n = x.text
        n2 = x.get('href')
        if (len(n) > 60):
            d1.append(n)
            href.append(n2)
            resp = requests.get(n2)
            soup2 = BeautifulSoup(resp.text, 'html.parser')
            for x in soup2.find_all('span'):
                if x.get('itemprop') == "dateModified":
                    y = x.text[9:22]
                    date.append(y)
                    # print(n,x.text[9:])
                    y = y.lstrip(':')
                    y = y.rstrip('I')
                    if (dateparser.parse(y) > d):
                        print(n, y)
    except:
        p = 1