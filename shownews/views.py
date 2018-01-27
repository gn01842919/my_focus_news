from django.shortcuts import render, redirect
from shownews.models import NewsData, ScrapingRule, NewsCategory


# Create your views here.
def homepage(request):
    return redirect('/news/')


def news(request):
    return render(request, 'news.html', {'all_news': NewsData.objects.all()})


def rules(request):
    return render(request, 'rules.html', {'all_rules': ScrapingRule.objects.all()})


def categories(request):
    return render(
        request, 'categories.html',
        {
            'all_categories': NewsCategory.objects.all(),
            'title_text': 'News Categories'
        }
    )


def news_by_category(request, category):

    target_tags = NewsCategory.objects.filter(name=category)

    target_rules = set()

    for tag in target_tags:
        target_rules.update(tag.scrapingrule_set.all())

    # print(target_rules)

    news_set = []

    for news in NewsData.objects.all():
        for rule in news.rules.all():
            if rule in target_rules:
                news_set.append(news)
                break

    return render(request, 'news.html', {'all_news': news_set})


def news_by_rule(request, rule_id):

    rule = ScrapingRule.objects.get(id=rule_id)

    return render(request, 'news.html', {'all_news': rule.newsdata_set.all()})
