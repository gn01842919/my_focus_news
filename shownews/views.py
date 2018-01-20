from django.shortcuts import render, redirect
from shownews.models import NewsData, ScrapingRule


# Create your views here.
def homepage(request):
    return redirect('/news/')


def news(request):
    return render(request, 'news.html', {'all_news': NewsData.objects.all()})


def rules(request):
    return render(request, 'rules.html', {'all_rules': ScrapingRule.objects.all()})
