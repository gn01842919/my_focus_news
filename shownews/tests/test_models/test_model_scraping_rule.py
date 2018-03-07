from django.test import TestCase
from shownews.models import ScrapingRule, NewsKeyword, NewsCategory, NewsData
from shownews import common_utils


class ScrapingRuleBasicTest(TestCase):

    def test_can_save_and_retrive(self):
        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')
        keyword1 = NewsKeyword.objects.create(name='keyword1')
        keyword2 = NewsKeyword.objects.create(name='keyword2', to_include=False)
        keyword3 = NewsKeyword.objects.create(name='keyword3')
        rule1.keywords.add(keyword1, keyword2)
        rule1.keywords.add(keyword2)
        rule1.keywords.add(keyword2)
        rule1.keywords.add(keyword3)
        tag1 = NewsCategory.objects.create(name='finance')
        tag2 = NewsCategory.objects.create(name='politics')
        rule1.tags.add(tag1, tag2)
        rule2.tags.add(tag2)

        # another rule
        rule2.keywords.add(keyword2, keyword3)

        # saved_rules = ScrapingRule.objects.all()

        self.assertEqual(ScrapingRule.objects.count(), 2)

        saved_rule_1 = ScrapingRule.objects.get(id=rule1.id)
        saved_rule_2 = ScrapingRule.objects.get(id=rule2.id)

        self.assertEqual(rule1, saved_rule_1)

        # same keyword objects will appear only once
        self.assertEqual(saved_rule_1.keywords.count(), 3)

        # Can retrieve the first keyword
        self.assertEqual(saved_rule_1.keywords.get(id=keyword1.id), keyword1)

        # Can retrieve the second keyword
        self.assertEqual(saved_rule_1.keywords.get(id=keyword2.id), keyword2)

        # The rule is active by default
        self.assertTrue(saved_rule_1.active)

        # The whole rule is correct
        self.assertEqual(
            saved_rule_1.details,
            "<Rule %d> [Active] Include (keyword1, keyword3), Exclude (keyword2), "
            "Tags (finance, politics)" % saved_rule_1.id
        )

        # Check that active can be set to False
        rule1.active = False
        rule1.full_clean()
        rule1.save()

        self.assertEqual(ScrapingRule.objects.count(), 2)

        saved_rule_1 = ScrapingRule.objects.get(id=rule1.id)
        saved_rule_2 = ScrapingRule.objects.get(id=rule2.id)

        self.assertEqual(saved_rule_1.keywords.count(), 3)
        self.assertFalse(saved_rule_1.active)

        self.assertEqual(
            saved_rule_1.details,
            "<Rule %d> [Inactive] Include (keyword1, keyword3), "
            "Exclude (keyword2), Tags (finance, politics)" % saved_rule_1.id
        )
        self.assertEqual(
            saved_rule_2.details,
            "<Rule %d> [Active] Include (keyword3), "
            "Exclude (keyword2), Tags (politics)" % saved_rule_2.id
        )

    def test_get_news_url(self):

        news = NewsData.objects.create(title='title1', url='http://url.com')
        rule = ScrapingRule.objects.create()
        news.rules.add(rule)
        self.assertEqual(rule.get_absolute_url(), '/news/rule/%d/' % rule.id)

    def test_get_sorted_related_news(self):

        news_data = common_utils.create_news_data_for_test(5)
        scraping_rules = common_utils.create_empty_rules_for_test(4)
        common_utils.create_scoremap_for_test(news_data, scraping_rules[:3])

        sorted_related_news_lists = {
            rule: rule.get_sorted_related_news()
            for rule in scraping_rules
        }

        for rule, news_list in sorted_related_news_lists.items():
            expected_sorted_news = common_utils.sort_news_by_scores_of_rules(
                news_data, (rule,), positive_only=True
            )
            self.assertEqual(len(expected_sorted_news), len(news_list))
            self.assertEqual(set(expected_sorted_news), set(news_list))
