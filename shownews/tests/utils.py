import random
from shownews import models


def get_news_sorted_by_scores_based_on_rules(news_data, scraping_rules):

    news_score_map = {}

    for news in news_data:
        total_score = 0
        for rule in scraping_rules:
            score = get_score_of_a_news_by_a_rule(news, rule)
            if score > 0:
                total_score += score

        news_score_map[news] = total_score

    return sorted(news_score_map, key=news_score_map.get, reverse=True)


def get_score_of_a_news_by_a_rule(news, rule):
    try:
        score_map = models.ScoreMap.objects.get(news=news, rule=rule)
    except models.ScoreMap.DoesNotExist:
        return 0

    return score_map.weight


def create_scoremap_for_test(news_data, scraping_rules):
    for news in news_data:
        for rule in scraping_rules:
            score = random.randint(-100, 100)
            models.ScoreMap.objects.create(news=news, rule=rule, weight=score)


def create_news_data_for_test(num, start_index=1, title_prefix="news_", url_prifix="http://test.url/"):
    return [
        models.NewsData.objects.create(
            title=title_prefix + str(i),
            url=url_prifix + str(i) + '/'
        )
        for i in range(start_index, num + start_index)
    ]


def create_empty_rules_for_test(num, prefix="rule_"):
    return [
        create_a_rule_for_test(name=prefix + str(i))
        for i in range(1, num + 1)
    ]


def create_a_rule_for_test(name, tags=None, keywords=None, is_active=True):
    rule = models.ScrapingRule.objects.create(name=name, active=is_active)

    if keywords:
        for kw in keywords:
            rule.keywords.add(kw)

    if tags:
        for tag in tags:
            rule.tags.add(tag)

    return rule


def create_tags_for_test(num, prefix="tag_"):
    return [
        models.NewsCategory.objects.create(name=prefix + str(i))
        for i in range(1, num + 1)
    ]


def create_keywords_for_test(num, prefix="keywords_", to_include=True):
    return [
        models.NewsKeyword.objects.create(name=prefix + str(i), to_include=to_include)
        for i in range(1, num + 1)
    ]
