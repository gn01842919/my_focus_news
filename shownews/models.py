from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from . import common_utils


class NewsCategory(models.Model):
    """A category for news.

    Note that objects of this class are often called "tag" in the program.

    """
    name = models.CharField(max_length=100, unique=True)

    @property
    def num_of_related_news(self):
        """Number of news that fall to this category (has this tag).
        """
        return len(self.get_sorted_related_news())

    def get_sorted_related_news(self):
        """Get all news that fall to this category in sorted order.

        News data are sorted by the sum of the related scraping rules.

        "Related rules" means the rules that has this tag (which means adding this tag to news).

        """
        target_rules = set(self.scrapingrule_set.all())

        related_news_data = set()

        for rule in target_rules:
            related_news_data.update(set(rule.get_sorted_related_news()))

        return common_utils.sort_news_by_scores_of_rules(
            related_news_data, target_rules
        )

    def get_absolute_url(self):
        """URL for the page to view all news that fall to this category (has this tag).
        """
        return reverse('news_by_category', args=[self.id])

    def __str__(self):
        return self.name


class NewsKeyword(models.Model):
    """A keyword for scraping rules to decide whether a news is of interested.

    Attributes:
        name (str): The keyword itself.
        to_include (bool): If True, a news with this keyword is likely to be of interest.
            If False, a news with this keyword is not of interest and should not be stored.

    """

    name = models.CharField(max_length=100)
    to_include = models.BooleanField(default=True)

    def __str__(self):
        return "{}({})".format(self.name, "include" if self.to_include else "exclude")

    class Meta:
        unique_together = ('name', 'to_include')


class ScrapingRule(models.Model):
    """A rule to decide whether a news is of interest.
    """
    name = models.CharField(max_length=100, default='', unique=True)
    active = models.BooleanField(default=True)
    keywords = models.ManyToManyField(NewsKeyword)
    tags = models.ManyToManyField(NewsCategory)

    @property
    def details(self):
        """Details of the rule, including its keywords and tags.
        """
        return (
            "<Rule {rule_id}> [{is_active}] Include ({kw_inc}), Exclude ({kw_exc}), Tags ({tags})"
            .format(
                rule_id=self.id,
                is_active="Active" if self.active else "Inactive",
                kw_inc=', '.join(k.name for k in self.keywords.all() if k.to_include),
                kw_exc=', '.join(k.name for k in self.keywords.all() if not k.to_include),
                tags=', '.join(t.name for t in self.tags.all())
            )
        )

    @property
    def num_of_related_news(self):
        """Number of news that are considered of interested by this rule.

        A news is considered of interested by a rule if the ScoreMap(news, rule)
        has a positive weight (score).

        """
        return len(self.get_sorted_related_news())

    def get_sorted_related_news(self):
        """Get all news that are considered of interested by this rule.

        News data are sorted by the score with this rule.

        """
        related_news_data = [
            score_map.news for score_map in ScoreMap.objects.filter(rule=self)
            if score_map.weight > 0
        ]
        return common_utils.sort_news_by_scores_of_rules(
            related_news_data, (self,)
        )

    def get_absolute_url(self):
        """URL for the page to view all news that are considered of interested by this rule.
        """
        return reverse('news_by_rule', args=[self.id])

    def __str__(self):
        return self.name + '  ' + self.details


class NewsData(models.Model):
    """A news
    """
    title = models.TextField(default='')
    url = models.URLField(unique=True, max_length=500)
    content = models.TextField(default='', blank=True)
    time = models.DateTimeField(default=timezone.now)
    read_time = models.DateTimeField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    # The rules which created this news
    rules = models.ManyToManyField(ScrapingRule)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time', '-creation_time']


class ScoreMap(models.Model):
    """This model records the weight (score) between a ScrapingRule and a NewsData.

    Score = 0 means the news is not considered of interest by the rule.
    Score > 0 means the news is of interest according to the rule.
    Score < 0 means the news should be excluded according to the rule.

    """
    news = models.ForeignKey(NewsData)
    rule = models.ForeignKey(ScrapingRule)
    weight = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    def __str__(self):
        return("['{}' : {}]  ==> {}".format(self.news.title, self.rule.name, self.weight))

    class Meta:
        ordering = ['-weight']
        unique_together = ('news', 'rule')
