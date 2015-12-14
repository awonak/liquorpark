from django.conf import settings
from django.shortcuts import render

from .forms import GiftCardForm
from .models import Article
from .utils.hours import BusinessHours
from .utils.events import events


def index(request):
    context = {
        'articles': Article.objects.all(),
        'events': events(),
        'hours': BusinessHours(settings.HOURS),
        'gift_card_form': GiftCardForm(request.POST),
    }
    return render(request, 'index.html', context)


def gift_card(request):
    context = {}

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GiftCardForm(request.POST)
        if form.is_valid():
            context.update({
                'name': form.cleaned_data['name'],
                'amount': form.cleaned_data['amount'],
            })

    return render(request, 'gift_card.html', context)


def gift_card_payment(request):
    context = {}

    return render(request, 'gift_card_payment.html', context)


def margincalc(request):
    return render(request, 'margincalc.html')
