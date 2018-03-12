"""Common utilities for the project and testing programs.
"""
import random
from shownews import models


def sort_news_by_scores_of_rules(news_data, scraping_rules, positive_only=False):
    """Sort news_data according to the sum of the scores for input scraping_rules.

    Note that only positive scores are taken into account.

    """
    news_score_map = {}

    for news in news_data:
        total_score = 0
        for rule in scraping_rules:
            score = get_score_of_a_news_by_a_rule(news, rule)
            if score > 0:
                total_score += score

        if positive_only and total_score <= 0:
            continue
        else:
            news_score_map[news] = total_score

    return sorted(news_score_map, key=news_score_map.get, reverse=True)


def get_score_of_a_news_by_a_rule(news, rule):
    """Get a news's score given by a rule.
    """
    try:
        score_map = models.ScoreMap.objects.get(news=news, rule=rule)
    except models.ScoreMap.DoesNotExist:
        return 0

    return score_map.weight


def create_scoremap_for_test(news_data, scraping_rules, allow_nonpositive_score=False):
    """Create testing data of model ``ScoreMap``.
    """
    for news in news_data:
        for rule in scraping_rules:
            set_scoremap(news, rule, allow_nonpositive_score)


def set_scoremap(news, rule, allow_nonpositive_score=False):
    """Set up a scoremap for a <news, rule> pair with randomized score for test.
    """
    if allow_nonpositive_score:
        min_score = -100
    else:
        min_score = 1
    news.rules.add(rule)
    score = random.randint(min_score, 100)
    models.ScoreMap.objects.create(news=news, rule=rule, weight=score)


def create_news_data_for_test(
    num, start_index=1, title_prefix="news_", url_prifix="http://test.url/"
):
    """Create testing data of model ``NewsData``.

    Args:
        num (int): Number of news_data to create.
        start_index (int): The starting index in the news titles.
        title_prefix (str, optional): Title prefix.
        url_prefix (str, optional): Url prefix.

    Returns:
        list(models.NewsData): Newly created news data for testing purpose.

    """
    return [
        models.NewsData.objects.create(
            title=title_prefix + str(i),
            url=url_prifix + str(i) + '/'
        )
        for i in range(start_index, num + start_index)
    ]


def create_empty_rules_for_test(num, prefix="rule_"):
    """Create testing data of model ``ScrapingRules`` with only rule name.

    Args:
        num (int): Number of news_data to create.
        prefix (str, optional): Prefix of the rule name.

    Returns:
        list(models.ScrapingRule): Newly created scraping rules for testing purpose.

    """
    return [
        create_a_rule_for_test(name=prefix + str(i))
        for i in range(1, num + 1)
    ]


def create_a_rule_for_test(name, tags=None, keywords=None, is_active=True):
    """Create an instance of ScrapingRule for test.
    """
    rule = models.ScrapingRule.objects.create(name=name, active=is_active)

    if keywords:
        for kw in keywords:
            rule.keywords.add(kw)

    if tags:
        for tag in tags:
            rule.tags.add(tag)

    return rule


def create_tags_for_test(num, prefix="tag_"):
    """Create a instance of NewsCategory (a tag) for test.
    """
    return [
        models.NewsCategory.objects.create(name=prefix + str(i))
        for i in range(1, num + 1)
    ]


def create_keywords_for_test(num, prefix="keywords_", to_include=True):
    """Create a instance of NewsKeyword for test.
    """
    return [
        models.NewsKeyword.objects.create(name=prefix + str(i), to_include=to_include)
        for i in range(1, num + 1)
    ]
