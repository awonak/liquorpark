import os
import requests
import sendgrid
from dateutil.parser import parse

from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, redirect

from .models import Article


def _events():

    events = cache.get('events')

    if not events:

        # Next 10 Events:
        url = 'https://www.googleapis.com/calendar/v3/calendars/drinkliquorpark.com_vo211klng2c69ho2lafbqr91io%40group.calendar.google.com/events?maxResults=3&orderBy=startTime&singleEvents=true&timeMin={}T00:00:00-07:00&key={}'.format(
            datetime.now().strftime("%Y-%m-%d"),
            settings.CAL_API_KEY,
        )
        events = requests.get(url)
        events = events.json().get('items', [])

        date_fmt = "%A %g/%-d/%Y"
        time_fmt = "%-I:%M %p"

        for e in events:
            if 'date' in e['start']:
                e['start']['date'] = parse(e['start']['date']).strftime(date_fmt)
            if 'dateTime' in e['start']:
                e['start']['date'] = parse(e['start']['dateTime']).strftime(date_fmt)
                e['start']['dateTime'] = parse(e['start']['dateTime']).strftime(time_fmt)
            if 'date' in e['end']:
                e['end']['date'] = parse(e['end']['date']).strftime(date_fmt)
            if 'dateTime' in e['end']:
                e['end']['date'] = parse(e['end']['dateTime']).strftime(date_fmt)
                e['end']['dateTime'] = parse(e['end']['dateTime']).strftime(time_fmt)

        cache.set('events', events, settings.CACHE_SHORT)

    return events


def index(request):
    context = {
        'articles': Article.objects.all(),
        'events': _events(),
    }
    return render(request, 'index.html', context)


def contact(request):
    status = None
    msg = None
    # form submission
    if request.method == "POST":
        # send email to team@drinkliquorpark.com
        sg = sendgrid.SendGridClient(
            os.getenv('SENDGRID_USERNAME'),
            os.getenv('SENDGRID_PASSWORD')
        )
        message = sendgrid.Mail()
        message.add_to('team@drinkliquorpark.com')
        message.set_subject('Contact Submission from drinkliquorpark.com')
        message.set_text(request.POST.get('message'))
        message.set_from(request.POST.get('from'))
        status, msg = sg.send(message)
        if status == 200:
            return redirect('contact-thanks')

    return render(request, 'contact.html', msg)


def contact_thanks(request):
    return render(request, 'contact-thanks.html')


def margincalc(request):
    return render(request, 'margincalc.html')
