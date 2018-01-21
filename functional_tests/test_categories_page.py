from .base import FunctionalTest
from shownews.models import NewsCategory


class CategoriesPageTest(FunctionalTest):

    def test_can_view_categories(self):

        tag_names = ['Finance', 'Politics']

        # Create data for testing
        NewsCategory.objects.create(name=tag_names[0])
        NewsCategory.objects.create(name=tag_names[1])

        # Go to rules page
        self.browser.get(self.live_server_url + '/categories/')

        # See the browser title and the header
        self.assertIn('My Focus News!', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('News Categories', header_text)

        # There is a table containing current rules
        categories_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_categories_table')
        )

        # Found the list of categories
        rows = categories_table.find_elements_by_tag_name('tr')
        self.assertTrue(rows)

        for index, row in enumerate(rows):
            rule = row.find_element_by_css_selector('.news_category')
            self.assertEqual(rule.text, tag_names[index])

        # Click the "Finance" link, and see all news under this category
        categories_table.find_element_by_link_text('Finance').click()

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                'Finance News'
            )
        )

        # Go back to the categories page
        self.browser.find_element_by_link_text('News Categories').click()

        categories_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_categories_table')
        )

        # Click the "Politics" link, and see all news under this category
        categories_table.find_element_by_link_text('Politics').click()

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                'Politics News'
            )
        )

        # Done
