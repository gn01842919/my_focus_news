from django.test import TestCase
from shownews.models import NewsData, ScrapingRule, NewsKeyword, NewsCategory


class HomepageTest(TestCase):

    def test_homepage_redirect_to_news(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/news/')


class NewsPageTest(TestCase):

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

    def test_display_news_for_given_category(self):
        tag1 = NewsCategory.objects.create(name='tag1')
        tag2 = NewsCategory.objects.create(name='tag2')
        tag3 = NewsCategory.objects.create(name='tag3')
        rule1 = ScrapingRule.objects.create()
        rule2 = ScrapingRule.objects.create()
        rule1.tags.add(tag1, tag2)
        rule2.tags.add(tag1, tag3)
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')

        news1.rules.add(rule1)
        news2.rules.add(rule2)

        # tag1 ==> news1, news2
        # tag2 ==> news1
        # tag3 ==> news2

        # Test the page for tag1
        response = self.client.get('/news/category/%s/' % tag1.id)
        self.assertTemplateUsed(response, 'news.html')
        self.assertIsInstance(response.context['all_news'][0], NewsData)
        self.assertIsInstance(response.context['all_news'][1], NewsData)
        self.assertContains(response, news1.title)
        self.assertContains(response, news2.title)

        # Test the page for tag2
        response = self.client.get('/news/category/%s/' % tag2.id)
        self.assertContains(response, news1.title)
        self.assertNotContains(response, news2.title)

        # Test the page for tag3
        response = self.client.get('/news/category/%s/' % tag3.id)
        self.assertNotContains(response, news1.title)
        self.assertContains(response, news2.title)

    def test_display_news_for_given_rule_id(self):
        rule1 = ScrapingRule.objects.create()
        rule2 = ScrapingRule.objects.create()
        rule3 = ScrapingRule.objects.create()
        news1 = NewsData.objects.create(title='Title 1', url='http://url1.com')
        news2 = NewsData.objects.create(title='Title 2', url='http://url2.com')
        news1.rules.add(rule1, rule3)
        news2.rules.add(rule2, rule3)

        response = self.client.get('/news/rule/%d/' % rule1.id)
        self.assertContains(response, news1.title)
        self.assertNotContains(response, news2.title)

        response = self.client.get('/news/rule/%d/' % rule2.id)
        self.assertContains(response, news2.title)
        self.assertNotContains(response, news1.title)

        response = self.client.get('/news/rule/%d/' % rule3.id)
        self.assertContains(response, news2.title)
        self.assertContains(response, news1.title)


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
