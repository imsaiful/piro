from django.shortcuts import render
from .models import HeadLine


def index(request):
    queryset = HeadLine.objects.all()
    context = {
        "post": queryset
    }
    return render(request, 'feed/index.html', context)
