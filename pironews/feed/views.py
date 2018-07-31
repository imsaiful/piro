from django.shortcuts import render
from .models import Republicdb, Indiatvdb, NDTVdb
import requests
from django.utils import timezone
from django.http import HttpResponse
from bs4 import BeautifulSoup

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
    print("Republic")
    url = 'https://www.republicworld.com/'
    resp = requests.get(url)
    list=[]
    soup = BeautifulSoup(resp.text, 'html.parser')
    for x in soup.find_all('a'):
        try:
            n = x.text
            if len(n) > 60:
                post = Republicdb(title=n, created_date=timezone.now(), published_date=timezone.now())
                post.save()
        except:
            p = 1
    print(list)
    return HttpResponse("<h1>Success</h1>")


def indiatv(request):
    print("india tv")
    url = 'https://www.indiatoday.in/'
    k= False
    resp = requests.get(url)
    print(resp.status_code)
    list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    for x in soup.find_all('a'):
        try:
            n = x.get('title')
            if (len(n) > 60):
                post = Indiatvdb(title=n, created_date=timezone.now(), published_date=timezone.now())
                post.save()
        except:
            p = 1
        print(list)
        return HttpResponse("<h1>Success</h1>")


def ndtv(request):
    print("ndtv")
    url = 'https://www.ndtv.com/'
    resp = requests.get(url)
    list=[]
    soup = BeautifulSoup(resp.text, 'html.parser')
    for x in soup.find_all('a'):
        try:
            n = x.text
            if (len(n) > 60):
                post = NDTVdb(title=n, created_date=timezone.now(), published_date=timezone.now())
                post.save()
        except:
            p = 1
    return HttpResponse("<h1>Success</h1>")
