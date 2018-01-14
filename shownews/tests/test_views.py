from django.test import TestCase


class HomepageTest(TestCase):
    def test_uses_news_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'news.html')

    def test_redirect_to_news(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/news/')
