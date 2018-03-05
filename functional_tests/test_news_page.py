from .base import FunctionalTest
from shownews.tests import utils
from shownews.tests.test_views import _create_testing_scraping_rules_and_newsdata


class NewsPageTest(FunctionalTest):

    def test_news_are_sored_by_scores(self):

        # Create data for testing, including ScoreMap
        news_data, scraping_rules = _create_testing_scraping_rules_and_newsdata()

        sorted_news = utils.get_news_sorted_by_scores_based_on_rules(
            news_data, scraping_rules
        )

        titles_expected = [news.title for news in sorted_news]

        # Go to /news/ and get news titles in the page
        self.browser.get(self.live_server_url + '/news/')

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

        # Done

    def test_can_view_all_the_news(self):

        # Create data for testing
        news_data = utils.create_news_data_for_test(2)

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
        news_data = utils.create_news_data_for_test(2)

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
        more_news_data = utils.create_news_data_for_test(2, start_index=3)

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
