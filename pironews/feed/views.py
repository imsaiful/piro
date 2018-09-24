from __future__ import print_function

from threading import Thread

from django.shortcuts import render
from .models import Republicdb, Hindustan_db, NDTVdb
from django.utils import timezone
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime, timedelta
from .models import NDTVdb
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views import generic
import sys  # used for the storage class
import requests
import base64  # used for encoding string
import urllib.parse  # used for enconding
from time import gmtime, strftime  # used for gathering time
from subprocess import call, check_output
from .twitter import main
import schedule
import time

x = 0
y = 0
z = 0

#second phace now begin with the scrapy
def index(request):
    republic_list = Republicdb.objects.order_by('-created_date')[0:5]
    hindustan_times_list = Hindustan_db.objects.order_by('-created_date')[0:5]
    ndtv_list = NDTVdb.objects.order_by('-created_date')[0:5]

    context = {
        'republic_posts': republic_list,
        'hindustan_posts': hindustan_times_list,
        'ndtv_posts': ndtv_list,
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
    return HttpResponse("<h1>Success Republic</h1>")


def indiatv(request):
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
                            qs = Hindustan_db(title=n, href=n2)
                            qs.save()
                            print(n, y)
                        break
        except:
            p = 1
    return HttpResponse("<h1>Success Hindustan</h1>")



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
                            qs = NDTVdb(title=n, href=n2)
                            qs.save()

                            print(n, y)
                            break
        except:
            p = 1
    return HttpResponse("<h1>Success NDTV</h1>")


def Republic_Home(request):
    qs = Republicdb.objects.all()
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        "news": qs,
        "Name": 'Republic',

    }
    return render(request, "feed/News_Home.html", context)


def Hindustan_Home(request):
    print("hindustanHome")
    qs = Hindustan_db.objects.all()
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)
    context = {
        "news": qs,
        "Name": 'Hindutan Times',
    }

    return render(request, "feed/News_Home.html", context)


def Ndtv_Home(request):
    print("hindustanHome")
    qs = NDTVdb.objects.all()
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)
    context = {
        "news": qs,
        "Name": 'NDTV',
    }

    return render(request, "feed/News_Home.html", context)


def twitter_trend(request):
    tweet, url = main()

    context = {
        'tweets_urls': zip(tweet, url),
    }
    print(context)
    return render(request, "feed/trends.html", context)


schedule.every().day.at("23:43").do(republic, requests)
schedule.every().day.at("23:45").do(indiatv, requests)
schedule.every().day.at("23:47").do(ndtv, requests)


class ScheduleThread(Thread):
    @classmethod
    def run(cls):
        while True:
            schedule.run_pending()
            time.sleep(10)


ScheduleThread().start()
