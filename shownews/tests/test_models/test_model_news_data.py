from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import pytz
from shownews.models import NewsData, ScrapingRule, NewsKeyword, NewsCategory


def create_news_data_with_ordering():

    num = 10
    titles = ['title_%s' % i for i in range(num)]
    urls = ['http://%s.com' % title for title in titles]
    base_time = timezone.now() - timedelta(days=num)
    time_list = [base_time + timedelta(days=i) for i in range(num)]

    news_data = [
        NewsData.objects.create(
            title=titles[0], url=urls[0],
        ),
        NewsData.objects.create(
            title=titles[1], url=urls[1], time=time_list[5]
        ),
        NewsData.objects.create(
            title=titles[2], url=urls[2], time=time_list[2]
        ),
        NewsData.objects.create(
            title=titles[3], url=urls[3], time=time_list[0]
        ),
        NewsData.objects.create(
            title=titles[4], url=urls[4], time=time_list[4]
        ),
        NewsData.objects.create(
            title=titles[5], url=urls[5], read_time=time_list[1]
        ),
        NewsData.objects.create(
            title=titles[6], url=urls[6], time=time_list[5]
        ),
    ]

    # Adjust creation_time because all may be created within 1 second...
    news_data[0].creation_time -= timedelta(days=1)
    news_data[0].save()
    news_data[1].creation_time -= timedelta(days=1)
    news_data[1].save()

    expected_ordering = [
        news_data[5],
        news_data[0],
        news_data[6],
        news_data[1],
        news_data[4],
        news_data[2],
        news_data[3],
    ]

    return news_data, expected_ordering


class NewsDataBasicTest(TestCase):

    def test_can_save_and_retrive(self):

        news = NewsData()
        news.title = 'A Breaking News'
        news.url = 'http://www.google.com'
        news.time = timezone.now()
        news.read_time = timezone.now()
        news.save()
        rule = ScrapingRule.objects.create()
        news.rules.add(rule)

        saved_news = NewsData.objects.first()
        self.assertEqual(news, saved_news)
        self.assertEqual(news.rules.first(), rule)

    def test_ordering(self):
        """
        News should be ordered by:
            1. time (time of the news) (from new to old)
            2. creation_time
        """

        news_data, expected_ordering = create_news_data_with_ordering()

        saved_news = NewsData.objects.all()

        self.assertEqual(
            list(saved_news),
            expected_ordering
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
        news.time = datetime(2015, 7, 4, 12, 30, 51, tzinfo=pytz.UTC)
        news.save()
        news.full_clean()

        # time can be retrieved as a datetime object
        # Note that saved_time is of UTC timezone according to settings.py
        saved_time = NewsData.objects.first().time
        self.assertEqual(saved_time.strftime("%Y/%m/%d %H:%M:%S"), "2015/07/04 12:30:51")

    def test_read_time_can_be_empty(self):
        news = NewsData()
        news.title = 'Title'
        # read_time attribute is not set
        news.url = 'http://url1.com'
        news.save()
        news.full_clean()  # should not raise


class NewsDataTagsAndKeywordsTest(TestCase):

    def testTagsAndKeywords(self):
        news_data = NewsData()
        news_data.title = 'A Breaking News'
        news_data.url = 'http://www.google.com'
        news_data.save()

        k1 = NewsKeyword.objects.create(name='NAS')
        k2 = NewsKeyword.objects.create(name='Camera', to_include=False)
        k3 = NewsKeyword.objects.create(name='CPU')
        tag1 = NewsCategory.objects.create(name='finance')
        tag2 = NewsCategory.objects.create(name='politics')
        tag3 = NewsCategory.objects.create(name='taiwan')

        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')

        rule1.keywords.add(k1, k2)
        rule1.tags.add(tag1, tag2)

        rule2.keywords.add(k3)
        rule2.tags.add(tag2, tag3)

        news_data.rules.add(rule1, rule2)

        tags = set(tag.name for rule in news_data.rules.all()
                   for tag in rule.tags.all())
        keywords = set(str(k) for rule in news_data.rules.all()
                       for k in rule.keywords.all())

        self.assertEqual(tags, {'finance', 'politics', 'taiwan'})
        self.assertEqual(keywords, {'CPU(include)', 'Camera(exclude)', 'NAS(include)'})
