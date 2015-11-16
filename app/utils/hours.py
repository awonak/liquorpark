from datetime import datetime, time

DOW = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun",
}


class Hours(object):

    def __init__(self, dow, _open, _close):
        self.day_of_week = dow
        self._open = time(_open)
        self._close = time(_close)

    def _fmt(self, t):
        return t.strftime("%-I %p").lower()

    @property
    def open(self):
        return self._fmt(self._open)

    @property
    def close(self):
        return self._fmt(self._close)

    @property
    def dow(self):
        return DOW[self.day_of_week]

    def __unicode__(self):
        return "{} {} - {}".format(
            self.dow,
            self.open,
            self.close
        )

    def __repr__(self):
        return self.__unicode__()

    def open_now(self):
        today = datetime.now().weekday() == self.day_of_week
        open_now = self._open < datetime.now().time() <= self._close
        return today and open_now


class BusinessHours(list):

    def __init__(self, hours):
        for d, h in enumerate(hours):
            self.append(Hours(d, *h))

    def current(self):
        now = datetime.now()
        cur = self[now.weekday()]
        if now.hour < cur._open.hour:
            return "Closed. We will open at {} today".format(cur.open)
        elif now.hour > cur._close.hour:
            return "Closed at {} today".format(cur.close)
        else:
            return "Open Now until {}".format(cur.close)
