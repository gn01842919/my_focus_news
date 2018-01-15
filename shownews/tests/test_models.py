from django.test import TestCase
from shownews.models import NewsData
from django.utils import timezone
from datetime import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class NewsDataBasicTest(TestCase):

    def test_can_save_and_retrive(self):
        news = NewsData()
        news.title = 'A Breaking News'
        news.url = 'http://www.google.com'
        news.time = timezone.now()
        news.save()

        saved_news = NewsData.objects.all()
        self.assertEqual(news.title, saved_news[0].title)
        self.assertEqual(news.url, saved_news[0].url)
        self.assertEqual(news.time, saved_news[0].time)
        self.assertEqual(news, saved_news[0])


class NewsDataInputValueTest(TestCase):

    # To ensure that some fields cannot be empty
    def _assert_raises_validation_or_integrity_error(self, func):
        try:
            func()
        except (ValidationError, IntegrityError) as e:
            pass
        else:
            self.fail('Expected to raise ValidationError or IntegrityError')

    def test_title_and_input_ordering(self):

        someurl = 'https://abc.com'

        # test no title
        self._assert_raises_validation_or_integrity_error(
            lambda: NewsData.objects.create(url=someurl).full_clean()
        )
        self._assert_raises_validation_or_integrity_error(
            lambda: NewsData.objects.create(url=someurl, title='').full_clean()
        )
        news = NewsData.objects.create(title='!@#$%^&*()-_=+.~`\'\"\\|/?<>,', url=someurl)
        news = NewsData.objects.create(title='中文標題', url=someurl)

        self.fail('Some asserts')

    def test_url(self):

        sometitle = 'News title'

        # test no url
        self._assert_raises_validation_or_integrity_error(
            lambda: NewsData.objects.create(title=sometitle, url='').full_clean()
        )
        self._assert_raises_validation_or_integrity_error(
            lambda: NewsData.objects.create(title=sometitle).full_clean()
        )

        news = NewsData.objects.create(url='http://!@#$%^&*()-_=+.~`\'\"\\|/?<>,', title=sometitle)
        news = NewsData.objects.create(url='http://abc.com/中文連結', title=sometitle)

    def test_time(self):

        news = NewsData()
        news.title = 'News title'
        news.url = 'http://abc.com'

        news.time = timezone.now()
        news.save()

        # time can be modified
        news.time = datetime(2015, 7, 4, 12, 30, 51)
        news.save()

        # time can be retrieved as a datetime object
        # Note that saved_time is of UTC timezone according to settings.py
        saved_time = NewsData.objects.all()[0].time
        self.assertEqual(saved_time.strftime("%Y/%m/%d %H:%M:%S"), "2015/07/04 12:30:51")


