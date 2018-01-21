from django.conf.urls import url
from shownews.views import news, news_by_category

urlpatterns = [
    url(r'^$', news),
    url(r'^([^/]+)/$', news_by_category),
]
