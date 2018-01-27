from .base import FunctionalTest
from shownews.models import NewsData


class NewsPageTest(FunctionalTest):

    def test_can_view_all_the_news(self):

        # Create data for testing
        NewsData.objects.create(title='Title 1', url='http://url1.com')
        NewsData.objects.create(title='Title 2', url='http://url2.com')

        # Go to /news/all/
        self.browser.get(self.live_server_url + '/news/all/')

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('All News', header_text)

        # There is a table containing news titles, links, and date
        news_table = self.wait_for(lambda: self.browser.find_element_by_id('id_news_table'))

        rows = news_table.find_elements_by_tag_name('tr')
        self.assertTrue(rows)

        for index, row in enumerate(rows, 1):
            title = row.find_element_by_css_selector('.news_title')
            url = row.find_element_by_css_selector('.news_url')
            date = row.find_element_by_css_selector('.news_date')
            self.assertEqual(title.text, 'Title %d' % (index))
            self.assertEqual(url.text, 'http://url%d.com' % (index))
            self.assertTrue(date.text)

        # Done

    def test_only_display_unread_news_by_default(self):

        # There are already some news...
        NewsData.objects.create(title='Title 1', url='http://url1.com')
        NewsData.objects.create(title='Title 2', url='http://url2.com')

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

        for index, row in enumerate(rows, 1):
            title = row.find_element_by_css_selector('.news_title')
            url = row.find_element_by_css_selector('.news_url')
            date = row.find_element_by_css_selector('.news_date')
            self.assertEqual(title.text, 'Title %d' % (index))
            self.assertEqual(url.text, 'http://url%d.com' % (index))
            self.assertTrue(date.text)

        # More news are generated
        NewsData.objects.create(title='Title 3', url='http://url3.com')
        NewsData.objects.create(title='Title 4', url='http://url4.com')

        # refresh the page
        self.browser.refresh()

        # Only unread news are displayed
        news_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_news_table')
        )

        rows = news_table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 2)

        for index, row in enumerate(rows, 3):
            title = row.find_element_by_css_selector('.news_title')
            url = row.find_element_by_css_selector('.news_url')
            date = row.find_element_by_css_selector('.news_date')
            self.assertEqual(title.text, 'Title %d' % (index))
            self.assertEqual(url.text, 'http://url%d.com' % (index))
            self.assertTrue(date.text)

        # Done
