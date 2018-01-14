from django.shortcuts import render, redirect


# Create your views here.
def homepage(request):
    return redirect('/news/')


def news(request):
    return render(request, 'news.html')
