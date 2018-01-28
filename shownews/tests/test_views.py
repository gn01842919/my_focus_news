from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime
import pytz
from shownews.models import NewsData, ScrapingRule, NewsKeyword, NewsCategory
from shownews.tests.test_models.test_model_news_data import create_news_data_with_ordering


class HomepageTest(TestCase):

    def test_homepage_redirect_to_news(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('unread_news'))


class AllNewsPageTest(TestCase):

    def setUp(self):
        self.target_url = reverse('all_news')

    def test_template_used(self):
        response = self.client.get(self.target_url)
        self.assertTemplateUsed(response, 'news.html')

    def test_displays_all_the_news(self):
        news_data = [
            NewsData.objects.create(
                title='Title 1',
                url='http://url1.com'
            ),
            NewsData.objects.create(
                title='Title 2',
                url='http://url2.com'
            ),
            NewsData.objects.create(
                title='Title 3',
                url='http://url3.com',
                read_time=timezone.now(),
            ),
            NewsData.objects.create(
                title='Title 4',
                url='http://url4.com',
                time=datetime(2010, 7, 4, 12, 30, 51, tzinfo=pytz.UTC),
            ),
        ]

        response = self.client.get(self.target_url)

        self.assertEqual(len(response.context['news_set']), 4)

        for i, news in enumerate(news_data):
            self.assertIsInstance(response.context['news_set'][i], NewsData)
            self.assertContains(response, news.title)

    def test_ordering(self):

        news_data, expected_ordering = create_news_data_with_ordering()

        response = self.client.get(self.target_url)
        responsed_news = response.context['news_set']

        self.assertEqual(len(responsed_news), len(expected_ordering))
        self.assertEqual(list(responsed_news), expected_ordering)


class UnreadNewsTest(TestCase):

    def setUp(self):
        self.target_url = reverse('unread_news')

    def test_template_used(self):
        response = self.client.get(self.target_url)
        self.assertTemplateUsed(response, 'news.html')

    def test_displays_only_unread_news(self):

        time1 = datetime(2017, 7, 4, 12, 30, 51, tzinfo=pytz.UTC)
        time2 = timezone.now()

        news = [
            NewsData.objects.create(
                title='Title 1', url='http://url1.com'
            ),
            NewsData.objects.create(
                title='Title 2', url='http://url2.com', read_time=time1
            ),
            NewsData.objects.create(
                title='Title 3', url='http://url3.com', read_time=time2
            ),
            NewsData.objects.create(
                title='Title 4', url='http://url4.com'
            ),
        ]

        response = self.client.get(self.target_url)

        self.assertEqual(len(response.context['news_set']), 2)

        self.assertContains(response, news[0].title)
        self.assertNotContains(response, news[1].title)
        self.assertNotContains(response, news[2].title)
        self.assertContains(response, news[3].title)

    def test_news_data_are_marked_as_read_once_shown_on_the_page(self):
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')

        self.assertIsNone(news1.read_time)
        self.assertIsNone(news2.read_time)

        self.client.get(self.target_url)

        # read_time is not None means that it has been read
        saved_news = NewsData.objects.all()
        self.assertIsNotNone(saved_news[0].read_time)
        self.assertIsNotNone(saved_news[1].read_time)

    def test_ordering(self):

        news_data, expected_ordering = create_news_data_with_ordering()

        response = self.client.get(self.target_url)
        responsed_news = response.context['news_set']

        expected_ordering = [news for news in expected_ordering if not news.read_time]

        self.assertEqual(len(responsed_news), len(expected_ordering))
        self.assertEqual(list(responsed_news), expected_ordering)


class SpecifiedNewsTest(TestCase):

    def test_template_used(self):
        # For NewsCategory
        tag1 = NewsCategory.objects.create(name='tag1')
        response = self.client.get(tag1.get_absolute_url())
        self.assertTemplateUsed(response, 'news.html')

        # For ScrapingRule
        rule1 = ScrapingRule.objects.create(name='rule1')
        response = self.client.get(rule1.get_absolute_url())
        self.assertTemplateUsed(response, 'news.html')

    def test_display_news_for_given_category_id(self):

        # Setup rules
        tag1 = NewsCategory.objects.create(name='tag1')
        tag2 = NewsCategory.objects.create(name='tag2')
        tag3 = NewsCategory.objects.create(name='tag3')
        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')
        rule1.tags.add(tag1, tag2)
        rule2.tags.add(tag1, tag3)

        # Setup news data
        news = [
            NewsData.objects.create(title='Title 1', url='http://url1.com'),
            NewsData.objects.create(title='Title 2', url='http://url2.com'),
        ]
        news[0].rules.add(rule1)
        news[1].rules.add(rule2)

        # Expected mappings:
        #     tag1 ==> news[0], news[1]
        #     tag2 ==> news[0]
        #     tag3 ==> news[1]

        # Test tag1's page
        response = self.client.get(tag1.get_absolute_url())

        self.assertEqual(len(response.context['news_set']), 2)

        for news_data in response.context['news_set']:
            self.assertIsInstance(news_data, NewsData)

        self.assertContains(response, news[0].title)
        self.assertContains(response, news[1].title)

        # Test tag2's page
        response = self.client.get(tag2.get_absolute_url())

        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news[0].title)
        self.assertNotContains(response, news[1].title)

        # Test tag3's page
        response = self.client.get(tag3.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertNotContains(response, news[0].title)
        self.assertContains(response, news[1].title)

    def test_display_news_for_given_rule_id(self):
        # create rules
        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')
        rule3 = ScrapingRule.objects.create(name='rule3')

        # create news data
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')
        news1.rules.add(rule1, rule3)
        news2.rules.add(rule2, rule3)

        # test rule1's page
        response = self.client.get(rule1.get_absolute_url())

        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news1.title)
        self.assertNotContains(response, news2.title)

        # test rule2's page
        response = self.client.get(rule2.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news2.title)
        self.assertNotContains(response, news1.title)

        # test rule3's page
        response = self.client.get(rule3.get_absolute_url())
        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, news2.title)
        self.assertContains(response, news1.title)


class RulesPageTest(TestCase):

    def setUp(self):
        self.target_url = reverse('rules')

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

        response = self.client.get(self.target_url)

        self.assertIsInstance(response.context['all_rules'][0], ScrapingRule)
        self.assertIsInstance(response.context['all_rules'][1], ScrapingRule)

        self.assertContains(response, 'keyword1')
        self.assertContains(response, 'keyword2')
        self.assertContains(response, 'keyword3')

        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')


class CategoriesPageTest(TestCase):

    def setUp(self):
        self.target_url = reverse('categories')

    def test_template_used(self):
        response = self.client.get(reverse('categories'))
        self.assertTemplateUsed(response, 'categories.html')

    def test_display_rules(self):
        NewsCategory.objects.create(name='tag1')
        NewsCategory.objects.create(name='tag2')

        response = self.client.get(self.target_url)

        self.assertIsInstance(response.context['all_categories'][0], NewsCategory)
        self.assertIsInstance(response.context['all_categories'][1], NewsCategory)

        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')
