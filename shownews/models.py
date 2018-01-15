from django.db import models
from django.utils import timezone


class NewsData(models.Model):
    title = models.TextField()
    url = models.URLField(unique=True)
    time = models.DateTimeField(default=timezone.now)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
