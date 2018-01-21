from django.test import TestCase
from shownews.models import ScrapingRule, NewsKeyword, NewsCategory


class ScrapingRuleBasicTest(TestCase):

    def test_can_save_and_retrive(self):
        rule1 = ScrapingRule.objects.create()
        rule2 = ScrapingRule.objects.create()
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

        saved_rules = ScrapingRule.objects.all()

        self.assertEqual(rule1, saved_rules[0])

        # same keyword objects will appear only once
        self.assertEqual(saved_rules[0].keywords.count(), 3)

        # Can retrieve the first keyword
        self.assertEqual(saved_rules[0].keywords.all()[0], keyword1)

        # Can retrieve the second keyword
        self.assertEqual(saved_rules[0].keywords.all()[1], keyword2)

        # The rule is active by default
        self.assertTrue(saved_rules[0].active)

        # The whole rule is correct
        self.assertEqual(str(saved_rules[0]), "[Active] Include (keyword1, keyword3), Exclude (keyword2), Tags (finance, politics)")

        # Check that active can be set to False
        rule1.active = False
        rule1.full_clean()
        rule1.save()

        saved_rules = ScrapingRule.objects.all()
        self.assertEqual(saved_rules[0].keywords.count(), 3)
        self.assertFalse(saved_rules[0].active)

        self.assertEqual(str(saved_rules[0]), "[Inactive] Include (keyword1, keyword3), Exclude (keyword2), Tags (finance, politics)")
        self.assertEqual(str(saved_rules[1]), "[Active] Include (keyword3), Exclude (keyword2), Tags (politics)")
