from .base import FunctionalTest
from shownews.tests import utils


class RulesPageTest(FunctionalTest):

    def test_can_view_rules(self):
        # Create data for testing
        keywords = utils.create_keywords_for_test(3)
        keywords.extend(utils.create_keywords_for_test(2, to_include=False))
        utils.create_a_rule_for_test(
            name='rule_1',
            keywords=keywords[1:4]
        )
        utils.create_a_rule_for_test(
            name='rule_2',
            keywords=[keywords[0], keywords[4]],
            is_active=False
        )

        # Go to rules page
        self.browser.get(self.live_server_url + '/rules/')

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Scraping Rules', header_text)

        # There is a table containing current rules
        rules_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_rules_table')
        )

        rows = rules_table.find_elements_by_tag_name('tr')

        self.assertTrue(rows)

        for rule in rows:
            self.assertIn('rule_', rule.text)

        # Done

    def test_click_rule_will_show_related_news(self):

        # Create testing data
        rules = utils.create_empty_rules_for_test(2)
        news_data = utils.create_news_data_for_test(3)

        news_data[0].rules.add(rules[0], rules[1])
        news_data[1].rules.add(rules[0])
        news_data[2].rules.add(rules[1])

        expected_url = self.live_server_url + '/news/rule/%d/'

        # Go to rules page
        self.browser.get(self.live_server_url + '/rules/')

        rules_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_rules_table')
        )

        # Click the first rule's link
        rules_table.find_element_by_link_text(rules[0].name).click()

        # Found the title is different
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                rules[0].name
            )
        )

        # Found that url is redirected to /news/rule/1/
        self.assertEqual(self.browser.current_url, expected_url % rules[0].id)

        # Go back to the rules page
        self.browser.find_element_by_link_text('Scraping Rules').click()

        rules_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_rules_table')
        )

        # The url is back to /rules/
        self.assertEqual(self.browser.current_url, self.live_server_url + '/rules/')

        # Click the second rule's link
        rules_table.find_element_by_link_text(rules[1].name).click()

        # Found the title is different
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                rules[1].name
            )
        )

        # Found that url is redirected to /news/rule/2/
        self.assertEqual(self.browser.current_url, expected_url % rules[1].id)

        # Done
