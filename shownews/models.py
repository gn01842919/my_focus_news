from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class NewsCategory(models.Model):
    # Note that objects of this class are often called "tag" in the program.

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news_by_category', args=[self.id])


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
    name = models.CharField(max_length=100, default='', unique=True)
    active = models.BooleanField(default=True)
    keywords = models.ManyToManyField(NewsKeyword)
    tags = models.ManyToManyField(NewsCategory)

    @property
    def details(self):
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

    def __str__(self):
        return self.name + '  ' + self.details

    def get_absolute_url(self):
        return reverse('news_by_rule', args=[self.id])


class NewsData(models.Model):
    title = models.TextField(default='')
    url = models.URLField(unique=True)
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
