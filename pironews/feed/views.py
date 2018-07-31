from django.shortcuts import render
from .models import Republicdb, Indiatvdb, NDTVdb
from django.utils import timezone
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime, timedelta
from .models import NDTVdb
from django.utils import timezone

def index(request):
    republicq = Republicdb.objects.all()
    Indiatvq = Indiatvdb.objects.all()
    ndtvq = NDTVdb.objects.all()
    context = {
        "republic_posts": republicq,
        "indiatv_posts": Indiatvq,
        "ndtv_posts": ndtvq,
    }
    return render(request, 'feed/index.html', context)


def republic(request):
    url = 'https://www.republicworld.com/india-news'
    print("Waiting for response")
    try:
        resp = requests.get(url)
    except:
        print("Error")
    print(resp)
    soup = BeautifulSoup(resp.text, 'html.parser')
    d1 = []
    href = []
    date = []
    d = datetime.now() - timedelta(1)
    for x in soup.find_all('a'):
        try:
            n = x.text.strip()
            n2 = x.get('href').strip()
            if (len(n) > 60):
                resp = requests.get(n2)
                soup2 = BeautifulSoup(resp.text, 'html.parser')

                for x in soup2.find_all('time'):
                    y = x.text[:14].strip()
                    if (dateparser.parse(y) > d):
                        qs = Republicdb(title=n, href=n2)
                        qs.save()
                        print(n, y)
                    break
        except:
            p = 1
    return HttpResponse("<h1>Success</h1>")


def indiatv(request):
    import requests
    from bs4 import BeautifulSoup
    import dateparser
    from datetime import datetime, timedelta
    url = 'https://www.hindustantimes.com/'

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    d1 = []
    href = []
    l = ['text-dt']
    d = datetime.now() - timedelta(1)
    for x in soup.find_all('a'):
        try:
            n = x.text
            n2 = x.get('href')
            if (len(n) > 60):
                d1.append(n.strip())
                href.append(n2.strip())
                resp = requests.get(n2)
                soup2 = BeautifulSoup(resp.text, 'html.parser')
                for x in soup2.find_all('span'):
                    if x.get('class') == l:
                        y = x.text[9:22].strip()
                        if (dateparser.parse(y) > d):
                            qs = Indiatvdb(title=n, href=n2)
                            qs.save()
                            print(n, y)
                        break
        except:
            p = 1
    print("Sorry")


def ndtv(request):
    url = 'https://www.ndtv.com'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    i = 1
    data = ""
    da = []
    d1 = []
    href = []
    date = []
    d = datetime.now() - timedelta(1)
    for x in soup.find_all('a'):

        try:
            n = x.text.strip()
            n2 = x.get('href').strip()
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
                            qs = NDTVdb(title=n , href=n2)
                            qs.save()

                            print(n, y)
                            break
        except:
            p = 1
    return HttpResponse("<h1>Success</h1>")
