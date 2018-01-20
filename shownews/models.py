from django.db import models
from django.utils import timezone


class NewsData(models.Model):
    title = models.TextField()
    url = models.URLField(unique=True)
    time = models.DateTimeField(default=timezone.now)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)


class NewsKeyword(models.Model):

    name = models.CharField(max_length=100)

    # True to include this keyword
    # False to exclude this keyword
    to_include = models.BooleanField(default=True)

    def __str__(self):
        return "{}({})".format(self.name, "include" if self.to_include else "exclude")

    class Meta:
        unique_together = ('name', 'to_include')


class ScrapingRule(models.Model):
    active = models.BooleanField(default=True)
    keywords = models.ManyToManyField(NewsKeyword)

    def __str__(self):
        output = "Include (" + ', '.join(k.name for k in self.keywords.all() if k.to_include)
        output += "), Exclude (" + ', '.join(k.name for k in self.keywords.all() if not k.to_include)
        output += ")"
        return output
