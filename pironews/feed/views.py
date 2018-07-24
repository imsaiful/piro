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


<<<<<<< HEAD
    toi_article = newspaper.build(url, language="en", memoize_articles=False)  # en for English
    at = []
    title = []
    for article in toi_article.articles[:50]:
        at.append(article)
    for x in at:
        try:
            x.download()
            x.parse()
            if (x.text != ""):
                title.append(x.title)
        except:
            p = 0
    i = 1
    #add to the db
    for x in title:
        post=HeadLine(title=x,created_date=timezone.now(), published_date=timezone.now())
        post.save()
=======
>>>>>>> d0c368a212539e43345503175f4485771b5cb7e8

    return HttpResponse("<h1>Hello World</h1>")
