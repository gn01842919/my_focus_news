from .base import FunctionalTest


class HomepageTest(FunctionalTest):

    def test_can_view_the_news_on_homepage(self):

        # Go to homepage
        self.browser.get(self.live_server_url)

        # Found the url is redirected to /news/
        expected_url = self.live_server_url + '/news/'
        self.assertEqual(self.browser.current_url, expected_url)

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('My Focus News', header_text)

        # There is a table containing news titles, links, and date
        news_table = self.wait_for(lambda: self.browser.find_element_by_id('id_news_table'))

        for row in news_table.find_elements_by_tag_name('tr'):
            title = row.find_element_by_css_selector('.news_title')
            link = row.find_element_by_css_selector('.news_link')
            date = row.find_element_by_css_selector('.news_date')
            print('News: {} {} {}'.format(title, link, date))
            self.assertIsNotNone(title)
            self.assertIsNotNone(link)
            self.assertIsNotNone(date)

        # Done
