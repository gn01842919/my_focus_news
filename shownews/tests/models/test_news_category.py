from django.test import TestCase
from shownews.models import ScrapingRule, NewsCategory, NewsData


class NewsCategoryBasicTest(TestCase):

    def test_can_save_and_retrive(self):
        # I trust django model......
        pass

    def test_get_news_url(self):

        news = NewsData.objects.create(title='title1', url='http://url.com')
        rule = ScrapingRule.objects.create()
        tag = NewsCategory.objects.create(name='TagName')
        rule.tags.add(tag)
        news.rules.add(rule)

        self.assertEqual(tag.get_absolute_url(), '/news/category/%s/' % tag.name)
