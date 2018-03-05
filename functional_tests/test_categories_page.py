from .base import FunctionalTest
from shownews.models import NewsCategory


class CategoriesPageTest(FunctionalTest):

    def test_can_view_categories(self):

        tag_names = ['Finance', '政治']

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

    def test_click_category_will_show_related_news(self):

        tag_names = ['Finance', '政治']
        expected_url = self.live_server_url + '/news/category/%d/'
        categories_page_url = self.live_server_url + '/categories/'

        # Create testing data
        tags = [
            NewsCategory.objects.create(name=tag_names[0]),
            NewsCategory.objects.create(name=tag_names[1])
        ]

        # Go to categories page
        self.browser.get(categories_page_url)

        categories_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_categories_table')
        )

        # Click the "Finance" link
        categories_table.find_element_by_link_text('Finance').click()

        # Found the title is different
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                'Finance News'
            )
        )

        # Found that url is redirected to /news/category/tag[0].id/
        self.assertEqual(self.browser.current_url, expected_url % (tags[0].id))

        # Go back to the categories page
        self.browser.find_element_by_link_text('News Categories').click()

        categories_table = self.wait_for(
            lambda: self.browser.find_element_by_id('id_categories_table')
        )

        # The url is back to /categories/
        self.assertEqual(self.browser.current_url, categories_page_url)

        # Click the "政治" link
        categories_table.find_element_by_link_text('政治').click()

        # Found the title is different
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_tag_name('h1').text,
                '政治 News'
            )
        )

        # The url is redirected to /news/category/tag[1].id/
        self.assertEqual(self.browser.current_url, expected_url % (tags[1].id))

        # Done
