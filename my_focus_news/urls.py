"""my_focus_news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from shownews.views import *

news_patterns = [
    url(r'^$', news),
    url(r'^category/([^/]+)/$', news_by_category, name='news_by_category'),
    url(r'^rule/(\d+)/$', news_by_rule, name='news_by_rule'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homepage, name='home'),
    url(r'^news/', include(news_patterns)),
    url(r'^rules/$', rules, name='rules'),
    url(r'^categories/$', categories, name='categories'),
]
