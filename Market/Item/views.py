from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
# Create your views here.

def index(request):
    return render(request, "Item/index.html")

def search(request):
    if request.method == "GET":
        title = request.GET.get('title', '')
        results = Item.objects.filter(title__icontains=title)

    context = {'results' : results,
               'title': title
            }

    return render(request, "Item/search.html", context)

def createItem(request):
    return render(request, "Item/createItem.html")

def create(request):
    pass