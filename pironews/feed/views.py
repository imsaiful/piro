from django.shortcuts import render
from .models import HeadLine
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.http import HttpResponse

def index(request):
    queryset = HeadLine.objects.all()
    context = {
        "posts": queryset
    }
    return render(request, 'feed/index.html', context)


def dbtimesofindia(request):
    url = 'https://www.indiatoday.in/'
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        for i in soup.find_all('a'):
            y = i.get('title')
            try:
                if len(y) > 40:
                    post = HeadLine(title=y, created_date=timezone.now(), published_date=timezone.now())
                    post.save()

            except:
                pass
    else:
        print("Error")



