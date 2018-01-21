from django.test import TestCase
from shownews.models import NewsData, ScrapingRule, NewsKeyword, NewsCategory


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

        rule1 = ScrapingRule.objects.create()
        rule2 = ScrapingRule.objects.create(active=False)
        keyword1 = NewsKeyword.objects.create(name='keyword1')
        keyword2 = NewsKeyword.objects.create(name='keyword2', to_include=False)
        keyword3 = NewsKeyword.objects.create(name='keyword3')
        tag1 = NewsCategory.objects.create(name='tag1')
        tag2 = NewsCategory.objects.create(name='tag2')

        rule1.keywords.add(keyword1, keyword2, keyword3)
        rule1.tags.add(tag1)
        rule2.keywords.add(keyword2, keyword3)
        rule2.tags.add(tag1, tag2)

        response = self.client.get('/rules/')

        self.assertIsInstance(response.context['all_rules'][0], ScrapingRule)
        self.assertIsInstance(response.context['all_rules'][1], ScrapingRule)

        self.assertContains(response, 'keyword1')
        self.assertContains(response, 'keyword2')
        self.assertContains(response, 'keyword3')

        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')


class CategoriesPageTest(TestCase):

    def test_uses_categories_template(self):
        response = self.client.get('/categories/')
        self.assertTemplateUsed(response, 'categories.html')

    def test_display_rules(self):
        NewsCategory.objects.create(name='tag1')
        NewsCategory.objects.create(name='tag2')

        response = self.client.get('/categories/')

        self.assertIsInstance(response.context['all_categories'][0], NewsCategory)
        self.assertIsInstance(response.context['all_categories'][1], NewsCategory)

        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')
