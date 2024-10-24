from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
    return render(request, "Item/index.html")

def search(request, title):
    context = "temp"
    return render(request, "Item/index.html")