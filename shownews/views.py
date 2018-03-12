from django.shortcuts import render, redirect
from django.utils import timezone
from shownews.models import NewsData, ScrapingRule, NewsCategory
from . import common_utils


def homepage(request):
    """Homepage redirects to "Unread News".
    """
    return redirect('/news/')


def unread_news(request):
    """Display unread News.

    Once displayed on this page, a news is considered "read", and will not be
    displayed on this page anymore.

    """

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
    """Display all the news in the database.

    Note that only news of interest are stored in the database.

    """
    all_rules = ScrapingRule.objects.all()
    sorted_news_data = common_utils.sort_news_by_scores_of_rules(NewsData.objects.all(), all_rules)

    return render(request, 'news.html', {
        'news_set': sorted_news_data,
        'page_title': 'All News',
    })


def rules(request):
    """Displays all scraping rules, and the number of news it considers of interest.

    Clicking a rule in this page will redirect to the page of ``news_by_rule()``.

    """
    return render(request, 'rules.html', {'all_rules': ScrapingRule.objects.all()})


def categories(request):
    """Displays all news categories (tags), and the number of news having this tag.

    Clicking a category in this page will redirect to the page of ``news_by_category()``.

    """
    return render(
        request, 'categories.html',
        {
            'all_categories': NewsCategory.objects.all(),
            'title_text': 'News Categories'
        }
    )


def news_by_category(request, tag_id):
    """Displays the news that falls into this category (in other words, has this tag).
    """
    tag = NewsCategory.objects.get(id=tag_id)

    return render(request, 'news.html', {
        'news_set': tag.get_sorted_related_news(),
        'page_title': tag.name + ' News',
    })


def news_by_rule(request, rule_id):
    """Displays the news that are considered of interest by this rule.
    """
    rule = ScrapingRule.objects.get(id=rule_id)

    return render(request, 'news.html', {
        'news_set': rule.get_sorted_related_news(),
        'page_title': rule.name,
    })
