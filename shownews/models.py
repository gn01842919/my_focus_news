from django.db import models
from django.utils import timezone


class NewsData(models.Model):
    title = models.TextField()
    url = models.URLField(unique=True)
    time = models.DateTimeField(default=timezone.now)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)


class ScrapingRule(models.Model):
    active = models.BooleanField(default=True)

    def __str__(self):
        pass


class NewsKeyword(models.Model):
    rule_id = models.ManyToManyField(ScrapingRule)
    name = models.CharField(max_length=100)

    # True to include this keyword
    # False to exclude this keyword
    to_include = models.BooleanField()

    class Meta:
        unique_together = ('name', 'to_include')
