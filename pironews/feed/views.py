from django.shortcuts import render
from .models import HeadLine
from newspaper import Article
import newspaper
from django.utils import timezone
from django.http import HttpResponse

def index(request):
    queryset = HeadLine.objects.all()
    context = {
        "posts": queryset
    }
    return render(request, 'feed/index.html', context)


def dbtimesofindia(request):
    print('in script')
    url = 'https://timesofindia.indiatimes.com/'

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

    return HttpResponse("<h1>Hello World</h1>")
