from .base import FunctionalTest


class HomepageAndNewsPageTest(FunctionalTest):

    def test_can_view_the_news_on_homepage(self):

        # Create data for testing
        self.create_news_data_for_test()

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

        # import time
        # time.sleep(50)

        rows = news_table.find_elements_by_tag_name('tr')
        self.assertTrue(rows)

        for row in rows:
            title = row.find_element_by_css_selector('.news_title')
            url = row.find_element_by_css_selector('.news_url')
            date = row.find_element_by_css_selector('.news_date')
            self.assertTrue(title.text)
            self.assertTrue(url.text)
            self.assertTrue(date.text)

        # Done
