from django.shortcuts import render, redirect
from shownews.models import NewsData


# Create your views here.
def homepage(request):
    return redirect('/news/')


def news(request):
    return render(request, 'news.html', {'all_news': NewsData.objects.all()})
