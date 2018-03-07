from .base import FunctionalTest
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


class NewsPageTest(FunctionalTest):

    def _given_rules_test_only_related_news_are_displayed_in_order(
        self, expected_news, target_url
    ):
        titles_expected = [news.title for news in expected_news]

        # Go to /news/ and get news titles in the page
        self.browser.get(target_url)

        news_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_news_table')
        )
        rows = news_table.find_elements_by_tag_name('tr')

        titles_found = []
        for index, row in enumerate(rows):
            td_title = row.find_element_by_css_selector('.news_title')
            titles_found.append(td_title.find_element_by_css_selector('a').text)

        # Make sure the sequence is as expected
        self.assertEqual(titles_found, titles_expected)

    def test_news_are_sorted_by_scores(self):

        # Create data for testing, including ScoreMap
        news_data, scraping_rules = _create_testing_scraping_rules_and_newsdata()

        sorted_news = common_utils.sort_news_by_scores_of_rules(
            news_data, scraping_rules
        )
        self._given_rules_test_only_related_news_are_displayed_in_order(
            sorted_news,
            self.live_server_url + '/news/'
        )
        self._given_rules_test_only_related_news_are_displayed_in_order(
            sorted_news,
            self.live_server_url + '/news/all/'
        )

        # For news created by a specified ScrapingRule
        taget_rule = scraping_rules[0]
        related_news = taget_rule.newsdata_set.all()

        sorted_related_news = common_utils.sort_news_by_scores_of_rules(
            related_news, (taget_rule,), positive_only=True
        )
        self._given_rules_test_only_related_news_are_displayed_in_order(
            sorted_related_news,
            self.live_server_url + '/news/rule/%s/' % taget_rule.id
        )

        # For news with a given tag
        target_tag = taget_rule.tags.all()[0]
        rules_having_target_tag = target_tag.scrapingrule_set.all()

        related_news = []
        for rule in rules_having_target_tag:
            related_news.extend(rule.newsdata_set.all())

        sorted_related_news = common_utils.sort_news_by_scores_of_rules(
            set(related_news), rules_having_target_tag, positive_only=True
        )
        self._given_rules_test_only_related_news_are_displayed_in_order(
            sorted_related_news,
            self.live_server_url + '/news/category/%s/' % target_tag.id
        )

    def test_can_view_all_the_news(self):

        # Create data for testing
        news_data = common_utils.create_news_data_for_test(2)

        # Go to /news/all/
        self.browser.get(self.live_server_url + '/news/all/')

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('All News', header_text)

        # There is a table containing news titles, links, and date
        news_table = self.wait_for(lambda: self.browser.find_element_by_id('id_news_table'))
        rows = news_table.find_elements_by_tag_name('tr')

        self.assertEqual(len(rows), 2)

        expected_titles = [news.title for news in news_data]
        expected_urls = [news.url for news in news_data]

        for index, row in enumerate(rows):
            td_title = row.find_element_by_css_selector('.news_title')
            title = td_title.find_element_by_css_selector('a').text
            url = td_title.find_element_by_css_selector('a').get_attribute('href')
            date = row.find_element_by_css_selector('.news_date').text
            self.assertIn(title, expected_titles)
            self.assertIn(url, expected_urls)
            self.assertTrue(date)

        # Done

    def test_only_display_unread_news_by_default(self):

        # There are already some news...
        news_data = common_utils.create_news_data_for_test(2)

        # Go to homepage
        self.browser.get(self.live_server_url)

        # Found the url is redirected to /news/
        expected_url = self.live_server_url + '/news/'
        self.assertEqual(self.browser.current_url, expected_url)

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Unread Focus News', header_text)

        # There is a table containing news titles, links, and date
        news_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_news_table')
        )

        rows = news_table.find_elements_by_tag_name('tr')

        self.assertEqual(len(rows), 2)

        expected_titles = [news.title for news in news_data]
        expected_urls = [news.url for news in news_data]

        for row in rows:
            td_title = row.find_element_by_css_selector('.news_title')
            title = td_title.find_element_by_css_selector('a').text
            url = td_title.find_element_by_css_selector('a').get_attribute('href')
            date = row.find_element_by_css_selector('.news_date').text
            self.assertIn(title, expected_titles)
            self.assertIn(url, expected_urls)
            self.assertTrue(date)

        # More news are generated
        more_news_data = common_utils.create_news_data_for_test(2, start_index=3)

        # refresh the page
        self.browser.refresh()

        # Only unread news are displayed
        news_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_news_table')
        )

        rows = news_table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 2)

        new_expected_titles = [news.title for news in more_news_data]
        new_expected_urls = [news.url for news in more_news_data]

        for row in rows:
            td_title = row.find_element_by_css_selector('.news_title')
            title = td_title.find_element_by_css_selector('a').text
            url = td_title.find_element_by_css_selector('a').get_attribute('href')
            date = row.find_element_by_css_selector('.news_date').text
            self.assertIn(title, new_expected_titles)
            self.assertNotIn(title, expected_titles)
            self.assertIn(url, new_expected_urls)
            self.assertNotIn(url, expected_urls)
            self.assertTrue(date)

        # Done
