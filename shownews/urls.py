from django.conf.urls import url
from shownews.views import news, news_by_category, news_by_rule

urlpatterns = [
    url(r'^$', news),
    url(r'^category/([^/]+)/$', news_by_category),
    url(r'^rule/(\d+)/$', news_by_rule),
]
