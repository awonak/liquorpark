from datetime import time
from django.test import TestCase
from django.conf import settings
from mock import Mock, patch

from app.utils.hours import BusinessHours, Hours


class HoursTestCase(TestCase):
    def setUp(self):
        self.bh = BusinessHours(settings.HOURS)

    def test_hours(self):
        for h in self.bh:
            self.assertTrue(isinstance(h, Hours))

    @patch('app.utils.hours.datetime')
    def test_early_current(self, mock_datetime):
        early = Mock()
        early.hour = 9
        early.weekday.return_value = 0
        mock_datetime.now.return_value = early
        self.assertEqual(
            self.bh.current(),
            "Closed. We will open at 1 PM today"
        )

    @patch('app.utils.hours.datetime')
    def test_open_current(self, mock_datetime):
        current = Mock()
        current.hour = 15
        current.weekday.return_value = 0
        mock_datetime.now.return_value = current
        self.assertEqual(
            self.bh.current(),
            "Open Now until 8 PM"
        )

    @patch('app.utils.hours.datetime')
    def test_late_current(self, mock_datetime):
        late = Mock()
        late.hour = 22
        late.weekday.return_value = 0
        mock_datetime.now.return_value = late
        self.assertEqual(
            self.bh.current(),
            "Closed at 8 PM today"
        )

    @patch('app.utils.hours.datetime')
    def test_open_now(self, mock_datetime):
        now = Mock()
        now.weekday.return_value = 0
        now.time.return_value = time(15)
        mock_datetime.now.return_value = now
        self.assertTrue(self.bh[0].open_now())

    @patch('app.utils.hours.datetime')
    def test_not_open_now(self, mock_datetime):
        now = Mock()
        now.weekday.return_value = 0
        now.time.return_value = time(22)
        mock_datetime.now.return_value = now
        self.assertFalse(self.bh[0].open_now())

    @patch('app.utils.hours.datetime')
    def test_not_open_tomorrow(self, mock_datetime):
        now = Mock()
        now.weekday.return_value = 1
        now.time.return_value = time(15)
        mock_datetime.now.return_value = now
        self.assertFalse(self.bh[0].open_now())
