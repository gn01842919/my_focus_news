from django.shortcuts import render, redirect
from django.utils import timezone
from shownews.models import NewsData, ScrapingRule, NewsCategory
from .tests import utils


def _sort_news_data_by_rules(news_data, scraping_rules):
    return utils.get_news_sorted_by_scores_based_on_rules(
        news_data, scraping_rules
    )


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
    sorted_unread_news_data = _sort_news_data_by_rules(unread_news, all_rules)

    return render(request, 'news.html', {
        'news_set': sorted_unread_news_data,
        'page_title': 'Unread Focus News',
    })


def all_news(request):
    all_rules = ScrapingRule.objects.all()
    sorted_news_data = _sort_news_data_by_rules(NewsData.objects.all(), all_rules)

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
    target_rules = set(tag.scrapingrule_set.all())

    related_news_data = []

    for news in NewsData.objects.all():
        for rule in news.rules.all():
            if rule in target_rules:
                score = utils.get_score_of_a_news_by_a_rule(news, rule)
                if score > 0:
                    related_news_data.append(news)

    sorted_related_news_data = _sort_news_data_by_rules(related_news_data, target_rules)

    return render(request, 'news.html', {
        'news_set': sorted_related_news_data,
        'page_title': tag.name + ' News',
    })


def news_by_rule(request, rule_id):

    rule = ScrapingRule.objects.get(id=rule_id)

    news_score_map = {
        news: utils.get_score_of_a_news_by_a_rule(news, rule)
        for news in rule.newsdata_set.all()
    }

    related_news_data = (news for news, score in news_score_map.items() if score > 0)

    sorted_related_news_data = _sort_news_data_by_rules(related_news_data, (rule,))

    return render(request, 'news.html', {
        'news_set': sorted_related_news_data,
        'page_title': rule.name,
    })
