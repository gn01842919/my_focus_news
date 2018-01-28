from django.shortcuts import render, redirect
from django.utils import timezone
from shownews.models import NewsData, ScrapingRule, NewsCategory

# Create your views here.
def homepage(request):
    return redirect('/news/')


def unread_news(request):

    unread_news = NewsData.objects.filter(read_time__isnull=True)

    curr_time = timezone.now()

    for news in unread_news:
        news.read_time = curr_time
        news.save()

    return render(request, 'news.html', {
        'news_set': unread_news,
        'page_title': 'Unread Focus News',
    })


def all_news(request):
    return render(request, 'news.html', {
        'news_set': NewsData.objects.all(),
        'page_title': 'All News',
    })


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


def news_by_category(request, tag_id):

    tag = NewsCategory.objects.get(id=tag_id)
    target_rules = set()

    target_rules.update(tag.scrapingrule_set.all())

    # print(target_rules)

    news_set = []

    for news in NewsData.objects.all():
        for rule in news.rules.all():
            if rule in target_rules:
                news_set.append(news)
                break

    return render(request, 'news.html', {
        'news_set': news_set,
        'page_title': tag.name + ' News',
    })


def news_by_rule(request, rule_id):

    rule = ScrapingRule.objects.get(id=rule_id)

    return render(request, 'news.html', {
        'news_set': rule.newsdata_set.all(),
        'page_title': rule.name,
    })
