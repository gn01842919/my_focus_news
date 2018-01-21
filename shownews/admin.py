from django.contrib import admin
from .models import NewsData, ScrapingRule, NewsKeyword, NewsCategory

admin.site.register(NewsData)
admin.site.register(ScrapingRule)
admin.site.register(NewsKeyword)
admin.site.register(NewsCategory)
