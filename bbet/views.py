from django.shortcuts import render
from django.conf import settings


def index(request):
    if settings.DEBUG:
        return render(request, 'index-dev.html')
    else:
        return render(request, 'index.html')



def home(request):
    return render(request, 'home.html')
