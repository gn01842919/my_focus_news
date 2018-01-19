from .base import FunctionalTest
from unittest import skip


class RulesPageTest(FunctionalTest):

    def test_can_view_rules(self):

        # Create data for testing
        self.create_news_data_for_test()

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
            self.assertTrue(rule.text)

        # Done

    # @skip
    # def test_can_edit_rules(self):

        # Go to rules page
        # self.browser.get('/rules/')

        # See an input area to add a rule
        # self.fail('to-do')
        # Add a rule

        # See the added rule

        # Add another rule

        # See the new rule

        # See the buttons to edite or delete a rule

        # Edit the second rule

        # See the updated rule

        # Delete the first rule

        # Now only the second rule exists

        # Delete it

        # No rules now

        # Done
