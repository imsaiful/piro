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
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    Model_one = Republicdb.objects.all()
    paginator = Paginator(Model_one, 6)
    page = request.GET.get('page1')
    try:
        Model_one = paginator.page(page)
    except PageNotAnInteger:
        Model_one = paginator.page(1)
    except EmptyPage:
        Model_one = paginator.page(paginator.num_pages)

    Model_two = Indiatvdb.objects.all()
    paginator = Paginator(Model_two, 6)
    page = request.GET.get('page2')
    try:
        Model_two = paginator.page(page)
    except PageNotAnInteger:
        Model_two = paginator.page(1)
    except EmptyPage:
        Model_two = paginator.page(paginator.num_pages)

    Model_three = NDTVdb.objects.all()
    paginator = Paginator(Model_two, 6)
    page = request.GET.get('page3')
    try:
        Model_three = paginator.page(page)
    except PageNotAnInteger:
        Model_three = paginator.page(1)
    except EmptyPage:
        Model_three = paginator.page(paginator.num_pages)

    context = {'republic_posts': Model_one, 'indiatv_posts': Model_two, 'ndtv_posts': Model_three}
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
    title = []
    d = datetime.now() - timedelta(1)
    print("Fetching News")
    for x in soup.find_all('a'):
        try:
            n = x.text.strip()
            n2 = x.get('href').strip()
            if (len(n) > 60):
                resp = requests.get(n2)
                soup2 = BeautifulSoup(resp.text, 'html.parser')

                for x in soup2.find_all('time'):
                    y = x.text.strip()
                    y = dateparser.parse(y)
                    y = str(y)
                    y = y[:10]
                    d = str(d)
                    d = d[:10]
                    if (y > d):
                        qs = Republicdb(title=n, href=n2)
                        qs.save()
                        print(n, y)
                        break
        except:
            p = 1
    print(title)
    print("Finished")
    return HttpResponse("<h1>Success NDTV</h1>")



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
    qs = Indiatvdb(title=n, href=n2)
    qs.save()
    print(n, y)


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
    return HttpResponse("<h1>Success NDTV</h1>")
