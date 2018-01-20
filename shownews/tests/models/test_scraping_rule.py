from django.test import TestCase
from shownews.models import ScrapingRule, NewsKeyword


class ScrapingRuleBasicTest(TestCase):

    def test_can_save_and_retrive(self):
        rule = ScrapingRule.objects.create()
        keyword1 = NewsKeyword.objects.create(name='keyword1')
        keyword2 = NewsKeyword.objects.create(name='keyword2', to_include=False)
        keyword3 = NewsKeyword.objects.create(name='keyword3')
        rule.keywords.add(keyword1, keyword2)
        rule.keywords.add(keyword2)
        rule.keywords.add(keyword2)
        rule.keywords.add(keyword3)

        saved_rule = ScrapingRule.objects.all()[0]

        # same keyword objects will appear only once
        self.assertEqual(saved_rule.keywords.count(), 3)

        # Can retrieve the first one
        self.assertEqual(saved_rule.keywords.all()[0], keyword1)

        # Can retrieve the second one
        self.assertEqual(saved_rule.keywords.all()[1], keyword2)

        # The rule is active by default
        self.assertTrue(saved_rule.active)

        # The whole rule is correct
        self.assertEqual(saved_rule.__str__(), "Include (keyword1, keyword3), Exclude (keyword2)")
