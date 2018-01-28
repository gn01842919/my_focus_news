"""
Purpose:
    Ensure that CSS is loaded.
    This does not really check the layout, because of TDD principles.
"""
from .base import FunctionalTest


class CSSLoadedTest(FunctionalTest):

    def test_layout_and_styling(self):

        # Go to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1920, 1080)

        nav = self.browser.find_element_by_tag_name('nav')
        hyperlink_tags = nav.find_elements_by_tag_name('a')

        y_values = [a.location['y'] for a in hyperlink_tags]

        # all y values should be equal
        for i in range(len(y_values) - 1):
            self.assertEqual(y_values[i], y_values[i + 1])

        # # The title is nicely centered
        # title = self.browser.find_element_by_tag_name('h1')
        # self.assertAlmostEqual(
        #     title.location['x'] + title.size['width'] / 2,
        #     1920 / 2,
        #     delta=1
        # )
