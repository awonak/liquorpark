import requests
from dateutil.parser import parse
from django.conf import settings
from django.core.cache import cache
from datetime import datetime


def events():

    events = cache.get('events')

    if not events:
        # Next 10 Events:
        url = 'https://www.googleapis.com/calendar/v3/calendars/drinkliquorpark.com_vo211klng2c69ho2lafbqr91io%40group.calendar.google.com/events?maxResults=3&orderBy=startTime&singleEvents=true&timeMin={}T00:00:00-07:00&key={}'.format(
            datetime.now().strftime("%Y-%m-%d"),
            settings.CAL_API_KEY,
        )
        events = requests.get(url, timeout=3)
        events = events.json().get('items', [])

        date_fmt = "%A %m/%-d/%Y"
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
