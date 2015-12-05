from django.conf import settings
from django.shortcuts import render

from .models import Article
from .utils.hours import BusinessHours
from .utils.events import events


def index(request):
    context = {
        'articles': Article.objects.all(),
        'events': events(),
        'hours': BusinessHours(settings.HOURS),
    }
    return render(request, 'index.html', context)


def margincalc(request):
    return render(request, 'margincalc.html')
