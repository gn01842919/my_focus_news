from .base import FunctionalTest
from shownews.models import ScrapingRule, NewsKeyword, NewsData


class RulesPageTest(FunctionalTest):

    def test_can_view_rules(self):

        # Create data for testing
        rule1 = ScrapingRule.objects.create(name='rule_name_1')
        rule2 = ScrapingRule.objects.create(active=False, name='rule_name_2')
        keyword1 = NewsKeyword.objects.create(name='keyword1')
        keyword2 = NewsKeyword.objects.create(name='keyword2', to_include=False)
        keyword3 = NewsKeyword.objects.create(name='keyword3')
        rule1.keywords.add(keyword1, keyword2, keyword3)
        rule2.keywords.add(keyword2, keyword3)

        # Go to rules page
        self.browser.get(self.live_server_url + '/rules/')

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Scraping Rules', header_text)

        # There is a table containing current rules
        rules_table = self.wait_for(lambda: self.browser.find_element_by_id('id_rules_table'))

        # import time
        # time.sleep(10)

        rows = rules_table.find_elements_by_tag_name('tr')

        self.assertTrue(rows)

        for rule in rows:
            self.assertIn('rule_name_', rule.text)

        # Done

    def test_click_rule_will_show_related_news(self):

        # Create testing data
        rule1 = ScrapingRule.objects.create(name='rule1')
        rule2 = ScrapingRule.objects.create(name='rule2')

        news1 = NewsData.objects.create(title='News1', url='http://url1.com')
        news2 = NewsData.objects.create(title='News2', url='http://url2.com')
        news3 = NewsData.objects.create(title='News3', url='http://url3.com')

        news1.rules.add(rule1, rule2)
        news2.rules.add(rule1)
        news3.rules.add(rule2)
        expected_url = self.live_server_url + '/news/rule/%d/'

        # Go to rules page
        self.browser.get(self.live_server_url + '/rules/')

        rules_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_rules_table')
        )

        # Click the first rule's link
        rules_table.find_element_by_link_text(rule1.name).click()

        # Found the title is different
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                rule1.name
            )
        )

        # Found that url is redirected to /news/rule/1/
        self.assertEqual(self.browser.current_url, expected_url % rule1.id)

        # Go back to the rules page
        self.browser.find_element_by_link_text('Scraping Rules').click()

        rules_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_rules_table')
        )

        # The url is back to /rules/
        self.assertEqual(self.browser.current_url, self.live_server_url + '/rules/')

        # Click the second rule's link
        rules_table.find_element_by_link_text(rule2.name).click()

        # Found the title is different
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                rule2.name
            )
        )

        # Found that url is redirected to /news/rule/2/
        self.assertEqual(self.browser.current_url, expected_url % rule2.id)

        # Done
