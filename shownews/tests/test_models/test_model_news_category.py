from django.test import TestCase
from shownews.models import ScrapingRule, NewsCategory, NewsData
from shownews import common_utils


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

        self.assertEqual(tag.get_absolute_url(), '/news/category/%d/' % tag.id)

    def test_get_sorted_related_news(self):

        tags = common_utils.create_tags_for_test(3)
        rules = [
            common_utils.create_a_rule_for_test("rule_0", tags=[tags[0]]),
            common_utils.create_a_rule_for_test("rule_1", tags=[tags[1]]),
            common_utils.create_a_rule_for_test("rule_2", tags=tags[:]),
            common_utils.create_a_rule_for_test("rule_3", tags=None),
            common_utils.create_a_rule_for_test("rule_4", tags=tags[1:3])
        ]
        news_data = common_utils.create_news_data_for_test(5)
        common_utils.set_scoremap(news_data[0], rules[0])
        common_utils.set_scoremap(news_data[1], rules[1])
        common_utils.set_scoremap(news_data[2], rules[1])
        common_utils.set_scoremap(news_data[2], rules[3])
        common_utils.set_scoremap(news_data[3], rules[2])
        common_utils.set_scoremap(news_data[4], rules[0])
        common_utils.set_scoremap(news_data[4], rules[2])

        # news with tags[0]:
        #       news_data[0], news_data[3], news_data[4]

        # Only test for tags[0]
        related_rules = tags[0].scrapingrule_set.all()

        expected_sorted_news = common_utils.sort_news_by_scores_of_rules(
            news_data, related_rules, positive_only=True
        )

        related_news = tags[0].get_sorted_related_news()

        self.assertEqual(len(expected_sorted_news), len(related_news))
        self.assertEqual(set(expected_sorted_news), set(related_news))
