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

    def test_ordering(self):

        news1 = NewsData.objects.create(title='t1', url='u1')
        news2 = NewsData.objects.create(title='t2', url='u2')
        news3 = NewsData.objects.create(title='t3', url='u3')

        self.assertEqual(news1.title, 't1')
        self.assertEqual(news1.url, 'u1')
        self.assertEqual(
            list(NewsData.objects.all()),
            [news1, news2, news3]
        )


class NewsDataInputValueTest(TestCase):

    def test_title(self):
        # no title
        with self.assertRaises(ValidationError):
            NewsData.objects.create(url='http://u1.com').full_clean()

        # empty title
        with self.assertRaises(ValidationError):
            NewsData.objects.create(url='http://u2.com', title='').full_clean()

        # no special charactor constraints
        NewsData.objects.create(title='--!@:#$%^&*()\t-_=+. ~`\'\"\\|/?<>,', url='http://u3.com').full_clean()

        # Chinese title
        NewsData.objects.create(title='中文標題', url='http://u4.com').full_clean()

    def test_url(self):
        news = NewsData()
        news.title = 'A Breaking News'

        # no url
        with self.assertRaises(ValidationError):
            news.full_clean()

        # empty url
        news.url = ''
        with self.assertRaises(ValidationError):
            news.full_clean()

        # Chinese url
        news.url = 'http://中文連結.com'
        news.full_clean()

        # url should be unique in DB
        news.save()
        with self.assertRaises(IntegrityError):
            NewsData.objects.create(url='http://中文連結.com', title='some title')

    def test_time(self):
        news = NewsData()
        news.title = 'News title'

        news.time = timezone.now()
        news.url = 'http://u1.com'

        news.save()

        # time can be modified
        news.time = datetime(2015, 7, 4, 12, 30, 51)
        news.save()
        news.full_clean()

        # time can be retrieved as a datetime object
        # Note that saved_time is of UTC timezone according to settings.py
        saved_time = NewsData.objects.all()[0].time
        self.assertEqual(saved_time.strftime("%Y/%m/%d %H:%M:%S"), "2015/07/04 12:30:51")