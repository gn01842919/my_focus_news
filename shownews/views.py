from django.shortcuts import render, redirect
from django.utils import timezone
from shownews.models import NewsData, ScrapingRule, NewsCategory
from . import common_utils


# Create your views here.
def homepage(request):
    return redirect('/news/')


def unread_news(request):

    unread_news = NewsData.objects.filter(read_time__isnull=True)

    curr_time = timezone.now()

    for news in unread_news:
        news.read_time = curr_time
        news.save()

    all_rules = ScrapingRule.objects.all()
    sorted_unread_news_data = common_utils.sort_news_by_scores_of_rules(
        unread_news, all_rules
    )

    return render(request, 'news.html', {
        'news_set': sorted_unread_news_data,
        'page_title': 'Unread Focus News',
    })


def all_news(request):
    all_rules = ScrapingRule.objects.all()
    sorted_news_data = common_utils.sort_news_by_scores_of_rules(NewsData.objects.all(), all_rules)

    return render(request, 'news.html', {
        'news_set': sorted_news_data,
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

    return render(request, 'news.html', {
        'news_set': tag.get_sorted_related_news(),
        'page_title': tag.name + ' News',
    })


def news_by_rule(request, rule_id):

    rule = ScrapingRule.objects.get(id=rule_id)

    return render(request, 'news.html', {
        'news_set': rule.get_sorted_related_news(),
        'page_title': rule.name,
    })
