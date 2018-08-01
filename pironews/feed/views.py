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
    republic_list = Republicdb.objects.all()
    Indiatv_list = Indiatvdb.objects.all()
    ndtv_list = NDTVdb.objects.all()
    republic_paginator = Paginator(republic_list, 5)
    Indiatv_paginator = Paginator(Indiatv_list, 5)  # Show 25 contacts per page
    ndtv__paginator = Paginator(ndtv_list , 5)
    republic_page = request.GET.get('page')
    indiatv_page =request.GET.get('page')
    ndtv_page = request.GET.get('page')
    try:
        republic_set = republic_paginator.page(republic_page )
        Indiatv_set =  Indiatv_paginator.page(indiatv_page)
        ndtv_set = ndtv__paginator.page(ndtv_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        republic_set = republic_paginator.page(1)
        Indiatv_set = Indiatv_paginator.page(1)
        ndtv_set = ndtv__paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        republic_set = republic_paginator.page(republic_paginator.num_pages)
        Indiatv_set =Indiatv_paginator .page(republic_paginator.num_pages)
        ndtv_set = ndtv__paginator.page(republic_paginator.num_pages)
    context = {
        "republic_posts": republic_set,
        "indiatv_posts": Indiatv_set,
        "ndtv_posts": ndtv_set,
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
