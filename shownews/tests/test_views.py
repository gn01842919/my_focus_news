from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime
import pytz
from shownews.models import NewsData, ScrapingRule, NewsCategory
from shownews import common_utils


def _create_testing_scraping_rules_and_newsdata():
    news_data = common_utils.create_news_data_for_test(10)
    tags = common_utils.create_tags_for_test(10)
    keywords = common_utils.create_keywords_for_test(10)
    scraping_rules = [
        common_utils.create_a_rule_for_test("rule1", tags=tags[:5], keywords=keywords[:5]),
        common_utils.create_a_rule_for_test("rule2", tags=tags[5:10], keywords=keywords[5:10]),
        common_utils.create_a_rule_for_test("rule3", tags=tags[2:6], keywords=keywords[2:6]),
        common_utils.create_a_rule_for_test("rule4", tags=tags, keywords=keywords),
    ]
    common_utils.create_scoremap_for_test(
        news_data, scraping_rules[:3], allow_nonpositive_score=True
    )
    return news_data, scraping_rules


def _create_testing_newsdata():
    news_data = common_utils.create_news_data_for_test(4)
    news_data.extend([
        NewsData.objects.create(
            title='news_5',
            url='http://test.url/5/',
            time=datetime(2017, 7, 4, 12, 30, 51, tzinfo=pytz.UTC),
        ),
        NewsData.objects.create(
            title='news_6',
            url='http://test.url/6/',
            read_time=timezone.now(),
        ),
        NewsData.objects.create(
            title='news_7',
            url='http://test_url.com/7/',
            read_time=datetime(2017, 7, 4, 12, 30, 51, tzinfo=pytz.UTC),
        )
    ])
    return news_data


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

    def test_displays_news(self):
        """
        Test displays all the news in DB
        """
        news_data = _create_testing_newsdata()

        response = self.client.get(self.target_url)

        self.assertEqual(len(response.context['news_set']), 7)

        for i, news in enumerate(news_data):
            self.assertIsInstance(response.context['news_set'][i], NewsData)
            self.assertContains(response, news.title)

    def test_news_are_ordered_by_score(self):
        news_data, scraping_rules = _create_testing_scraping_rules_and_newsdata()

        sorted_news = common_utils.sort_news_by_scores_of_rules(
            news_data, scraping_rules
        )

        response = self.client.get(self.target_url)
        responsed_news = list(response.context['news_set'])

        self.assertEqual(len(responsed_news), len(sorted_news))
        self.assertEqual(responsed_news, sorted_news)


class UnreadNewsTest(AllNewsPageTest):
    """Note that this inherits from AllNewsPageTest !!!!!
    """

    def setUp(self):
        self.target_url = reverse('unread_news')

    def test_displays_news(self):
        """
        Test only displays unread news data.
        """
        news_data = _create_testing_newsdata()

        response = self.client.get(self.target_url)
        self.assertEqual(len(response.context['news_set']), 5)

        for i in range(5):
            self.assertContains(response, news_data[i].title)
        for i in range(5, 7):
            self.assertNotContains(response, news_data[i].title)

    def test_news_data_are_marked_as_read_once_shown_on_the_page(self):
        for news in common_utils.create_news_data_for_test(5):
            self.assertIsNone(news.read_time)

        # visit the page
        self.client.get(self.target_url)

        # read_time is not None means that it has been read
        for news in NewsData.objects.all():
            self.assertIsNotNone(news.read_time)


class SpecifiedNewsTest(TestCase):

    def test_template_used(self):
        # For NewsCategory
        tag = common_utils.create_tags_for_test(1)[0]
        response = self.client.get(tag.get_absolute_url())
        self.assertTemplateUsed(response, 'news.html')

        # For ScrapingRule
        rule = common_utils.create_empty_rules_for_test(1)[0]
        response = self.client.get(rule.get_absolute_url())
        self.assertTemplateUsed(response, 'news.html')

    def test_news_with_given_rule_are_sorted_by_scores(self):
        news_data, scraping_rules = _create_testing_scraping_rules_and_newsdata()
        target_rule = scraping_rules[0]
        expected_news = target_rule.get_sorted_related_news()

        response = self.client.get(target_rule.get_absolute_url())
        responsed_news = list(response.context['news_set'])

        self.assertEqual(len(responsed_news), len(expected_news))
        self.assertEqual(responsed_news, expected_news)

    def test_news_with_given_tag_are_sorted_by_scores(self):

        news_data, scraping_rules = _create_testing_scraping_rules_and_newsdata()
        target_tag = scraping_rules[0].tags.all()[0]

        expected_news = target_tag.get_sorted_related_news()

        response = self.client.get(target_tag.get_absolute_url())
        responsed_news = list(response.context['news_set'])

        self.assertEqual(len(responsed_news), len(expected_news))
        self.assertEqual(responsed_news, expected_news)

    def test_displays_news_for_given_category_id(self):

        # Setup news_data and rules
        tags = common_utils.create_tags_for_test(3)
        rules = [
            common_utils.create_a_rule_for_test("rule_1", tags=tags[:2]),
            common_utils.create_a_rule_for_test("rule_2", tags=[tags[0], tags[2]])
        ]
        news_data = common_utils.create_news_data_for_test(2)
        common_utils.set_scoremap(news_data[0], rules[0])
        common_utils.set_scoremap(news_data[1], rules[1])

        tag_responses = [self.client.get(tag.get_absolute_url()) for tag in tags]

        # Test common properties for all tags
        for response in tag_responses:
            for news in response.context['news_set']:
                self.assertIsInstance(news, NewsData)

        # Expected mappings:
        #     tags[0] ==> news[0], news[1]
        #     tags[1] ==> news[0]
        #     tags[2] ==> news[1]

        # Test tags[0]'s page
        response = tag_responses[0]
        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, news_data[0].title)
        self.assertContains(response, news_data[1].title)

        # Test tags[1]'s page
        response = tag_responses[1]
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news_data[0].title)
        self.assertNotContains(response, news_data[1].title)

        # Test tag[2]'s page
        response = tag_responses[2]
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertNotContains(response, news_data[0].title)
        self.assertContains(response, news_data[1].title)

    def test_displays_news_for_given_rule_id(self):
        rules = common_utils.create_empty_rules_for_test(3)
        news_data = common_utils.create_news_data_for_test(2)
        common_utils.set_scoremap(news_data[0], rules[0])
        common_utils.set_scoremap(news_data[0], rules[2])
        common_utils.set_scoremap(news_data[1], rules[1])
        common_utils.set_scoremap(news_data[1], rules[2])

        rule_responses = [self.client.get(rule.get_absolute_url()) for rule in rules]

        # Test common properties for all rules
        for response in rule_responses:
            for news in response.context['news_set']:
                self.assertIsInstance(news, NewsData)

        # test rule[0]'s page
        response = rule_responses[0]
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news_data[0].title)
        self.assertNotContains(response, news_data[1].title)

        # test rule[1]'s page
        response = rule_responses[1]
        self.assertEqual(len(response.context['news_set']), 1)
        self.assertContains(response, news_data[1].title)
        self.assertNotContains(response, news_data[0].title)

        # test rule[2]'s page
        response = rule_responses[2]
        self.assertEqual(len(response.context['news_set']), 2)
        self.assertContains(response, news_data[1].title)
        self.assertContains(response, news_data[0].title)


class RulesPageTest(TestCase):

    def setUp(self):
        self.target_url = reverse('rules')

    def test_template_used(self):
        response = self.client.get(reverse('rules'))
        self.assertTemplateUsed(response, 'rules.html')

    def test_displays_rules(self):
        keywords = common_utils.create_keywords_for_test(3)
        keywords.extend(common_utils.create_keywords_for_test(2, to_include=False))

        tags = common_utils.create_tags_for_test(5)

        rules = [
            common_utils.create_a_rule_for_test(
                name='rule_1',
                keywords=keywords[1:4],
                tags=tags[:3]
            ),
            common_utils.create_a_rule_for_test(
                name='rule_2',
                keywords=[keywords[0], keywords[4]],
                tags=tags[3:],
                is_active=False
            )
        ]

        response = self.client.get(self.target_url)

        for rule in response.context['all_rules']:
            self.assertIsInstance(rule, ScrapingRule)

        for rule in rules:
            self.assertContains(response, rule.name)

        for keyword in keywords:
            self.assertContains(response, keyword.name)

        for tag in tags:
            self.assertContains(response, tag.name)


class CategoriesPageTest(TestCase):

    def setUp(self):
        self.target_url = reverse('categories')

    def test_template_used(self):
        response = self.client.get(reverse('categories'))
        self.assertTemplateUsed(response, 'categories.html')

    def test_display_rules(self):
        tags = common_utils.create_tags_for_test(5)

        response = self.client.get(self.target_url)

        for tag in response.context['all_categories']:
            self.assertIsInstance(tag, NewsCategory)

        for tag in tags:
            self.assertContains(response, tag)
