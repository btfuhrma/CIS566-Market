from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
from .models import ItemBuilder
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
    if request.method == "POST":
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        category = request.POST.get('category', '')
        image = request.POST.get('image', '')
        builder = ItemBuilder()
        builder.set_category(category)
        builder.set_description(description)
        builder.set_price(price)
        builder.set_title(title)
        builder.set_sold(False)
        builder.set_user(request.user)
        builder.set_image(image)
        builder.build()
    return render(request, "Item/index.html")