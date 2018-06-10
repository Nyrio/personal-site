from django.shortcuts import render
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponseRedirect("/about/")


def about(request):
    return render(request, "about.html")


def blog(request):
    return render(request, "blog.html")
