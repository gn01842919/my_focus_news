from .base import FunctionalTest
from shownews.models import NewsData
from shownews.tests import utils


class NewsPageTest(FunctionalTest):

    def test_news_are_sored_by_scores(self):

        # Create data for testing
        news_data = utils.create_news_data_for_test(5)
        tags = utils.create_tags_for_test(4)
        keywords = utils.create_keywords_for_test(4)
        scraping_rules = [
            utils.create_rule_for_test("rule1", tags=tags[:2], keywords=keywords[:2]),
            utils.create_rule_for_test("rule2", tags=tags[2:4], keywords=keywords[2:4]),
            utils.create_rule_for_test("rule3", tags=tags[1:3], keywords=keywords[1:3]),
            utils.create_rule_for_test("rule4", tags=tags, keywords=keywords),
        ]
        utils.create_scoremap_for_test(news_data, scraping_rules[:2])

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
        news_data = [
            NewsData.objects.create(title='Title 1', url='http://url1.com/'),
            NewsData.objects.create(title='Title 2', url='http://url2.com/'),
        ]

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
        news_data = [
            NewsData.objects.create(title='Title 1', url='http://url1.com/'),
            NewsData.objects.create(title='Title 2', url='http://url2.com/'),
        ]

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
        more_news_data = [
            NewsData.objects.create(title='Title 3', url='http://url3.com/'),
            NewsData.objects.create(title='Title 4', url='http://url4.com/'),
        ]

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
