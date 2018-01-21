from .base import FunctionalTest
from shownews.models import ScrapingRule, NewsKeyword
# from unittest import skip


class RulesPageTest(FunctionalTest):

    def test_can_view_rules(self):

        # Create data for testing
        rule1 = ScrapingRule.objects.create()
        rule2 = ScrapingRule.objects.create(active=False)
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

        for row in rows:
            rule = row.find_element_by_css_selector('.scraping_rule')
            self.assertTrue(rule.text)  # Should be adjust to use assertEqual someday...

        # Done
