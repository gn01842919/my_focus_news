from django.test import TestCase
from shownews.models import NewsData, ScrapingRule


class HomepageAndNewsPageTest(TestCase):

    def test_homepage_redirect_to_news(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/news/')

    def test_uses_news_template(self):
        response = self.client.get('/news/')
        self.assertTemplateUsed(response, 'news.html')

    def test_displays_news_data(self):
        NewsData.objects.create(title='Title 1', url='http://url1.com')
        NewsData.objects.create(title='Title 2', url='http://url2.com')

        response = self.client.get('/news/')

        # print(response.content.decode())

        self.assertContains(response, 'Title 1')
        self.assertContains(response, 'Title 2')

        self.assertIsInstance(response.context['all_news'][0], NewsData)

class RulesPageTest(TestCase):

    def test_uses_rules_template(self):
        response = self.client.get('/rules/')
        self.assertTemplateUsed(response, 'rules.html')

    def test_displays_rules(self):
        self.fail('to-do')
