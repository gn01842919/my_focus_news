from .base import FunctionalTest
from shownews.models import NewsCategory


class CategoriesPageTest(FunctionalTest):

    def test_can_view_categories(self):

        # Create data for testing
        NewsCategory.objects.create(name='tag1')
        NewsCategory.objects.create(name='tag2')

        # Go to rules page
        self.browser.get(self.live_server_url + '/categories/')

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('News Categories', header_text)

        # There is a table containing current rules
        categories_table = self.wait_for(lambda: self.browser.find_element_by_id('id_categories_table'))

        # import time
        # time.sleep(10)

        rows = categories_table.find_elements_by_tag_name('tr')

        self.assertTrue(rows)

        for row in rows:
            rule = row.find_element_by_css_selector('.news_category')
            self.assertTrue(rule.text)

        # Done
