from django.test import TestCase
from shownews.models import NewsData, ScrapingRule, NewsKeyword, NewsCategory
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime
import pytz


class HomepageTest(TestCase):

    def test_homepage_redirect_to_news(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('unread_news'))


class NewsPageTest(TestCase):

    def test_displays_all_the_news(self):
        NewsData.objects.create(title='Title 1', url='http://url1.com')
        NewsData.objects.create(title='Title 2', url='http://url2.com')

        response = self.client.get(reverse('all_news'))

        self.assertTemplateUsed(response, 'news.html')

        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, 'Title 1')
        self.assertContains(response, 'Title 2')
        self.assertIsInstance(response.context['news_set'][0], NewsData)

    def test_display_news_for_given_category_id(self):
        tag1 = NewsCategory.objects.create(name='tag1')
        tag2 = NewsCategory.objects.create(name='tag2')
        tag3 = NewsCategory.objects.create(name='tag3')
        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')
        rule1.tags.add(tag1, tag2)
        rule2.tags.add(tag1, tag3)
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')

        news1.rules.add(rule1)
        news2.rules.add(rule2)

        # tag1 ==> news1, news2
        # tag2 ==> news1
        # tag3 ==> news2

        # Test the page for tag1
        response = self.client.get(tag1.get_absolute_url())

        self.assertTemplateUsed(response, 'news.html')

        self.assertIsInstance(response.context['news_set'][0], NewsData)
        self.assertIsInstance(response.context['news_set'][1], NewsData)
        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, news1.title)
        self.assertContains(response, news2.title)

        # Test the page for tag2
        response = self.client.get(tag2.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news1.title)
        self.assertNotContains(response, news2.title)

        # Test the page for tag3
        response = self.client.get(tag3.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertNotContains(response, news1.title)
        self.assertContains(response, news2.title)

    def test_display_news_for_given_rule_id(self):
        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')
        rule3 = ScrapingRule.objects.create(name='rule3')
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')
        news1.rules.add(rule1, rule3)
        news2.rules.add(rule2, rule3)

        response = self.client.get(rule1.get_absolute_url())

        self.assertTemplateUsed(response, 'news.html')

        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news1.title)
        self.assertNotContains(response, news2.title)

        response = self.client.get(rule2.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news2.title)
        self.assertNotContains(response, news1.title)

        response = self.client.get(rule3.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, news2.title)
        self.assertContains(response, news1.title)

    def test_displays_only_unread_news(self):

        time1 = datetime(2017, 7, 4, 12, 30, 51, tzinfo=pytz.UTC)
        time2 = timezone.now()

        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com', read_time=time1)
        news3 = NewsData.objects.create(title='Title 3', url='http://url3.com', read_time=time2)
        news4 = NewsData.objects.create(title='Title 4', url='http://url4.com')

        response = self.client.get(reverse('unread_news'))

        self.assertTemplateUsed(response, 'news.html')

        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, news1.title)
        self.assertNotContains(response, news2.title)
        self.assertNotContains(response, news3.title)
        self.assertContains(response, news4.title)

    def test_news_data_are_marked_as_read_once_shown_on_the_page(self):
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')

        self.assertIsNone(news1.read_time)
        self.assertIsNone(news2.read_time)

        self.client.get(reverse('unread_news'))

        # read_time is not None means that it has been read
        saved_news = NewsData.objects.all()
        self.assertIsNotNone(saved_news[0].read_time)
        self.assertIsNotNone(saved_news[1].read_time)




class RulesPageTest(TestCase):

    def test_template_used(self):
        response = self.client.get(reverse('rules'))
        self.assertTemplateUsed(response, 'rules.html')

    def test_displays_rules(self):

        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2', active=False)
        keyword1 = NewsKeyword.objects.create(name='keyword1')
        keyword2 = NewsKeyword.objects.create(name='keyword2', to_include=False)
        keyword3 = NewsKeyword.objects.create(name='keyword3')
        tag1 = NewsCategory.objects.create(name='tag1')
        tag2 = NewsCategory.objects.create(name='tag2')

        rule1.keywords.add(keyword1, keyword2, keyword3)
        rule1.tags.add(tag1)
        rule2.keywords.add(keyword2, keyword3)
        rule2.tags.add(tag1, tag2)

        response = self.client.get(reverse('rules'))

        self.assertIsInstance(response.context['all_rules'][0], ScrapingRule)
        self.assertIsInstance(response.context['all_rules'][1], ScrapingRule)

        self.assertContains(response, 'keyword1')
        self.assertContains(response, 'keyword2')
        self.assertContains(response, 'keyword3')

        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')


class CategoriesPageTest(TestCase):

    def test_template_used(self):
        response = self.client.get(reverse('categories'))
        self.assertTemplateUsed(response, 'categories.html')

    def test_display_rules(self):
        NewsCategory.objects.create(name='tag1')
        NewsCategory.objects.create(name='tag2')

        response = self.client.get(reverse('categories'))

        self.assertIsInstance(response.context['all_categories'][0], NewsCategory)
        self.assertIsInstance(response.context['all_categories'][1], NewsCategory)

        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')
