from django.test import TestCase


class HomepageAndNewsTest(TestCase):

    def test_homepage_redirect_to_news(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/news/')

    def test_uses_news_template(self):
        response = self.client.get('/news/')
        self.assertTemplateUsed(response, 'news.html')
