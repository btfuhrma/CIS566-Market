from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
from .models import ItemBuilder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# Create your views here.

from .models import Item, Purchase, Cart

def index(request):
    return render(request, "Item/index.html")

@login_required
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)  # Retrieve items in the cart for the user
    return render(request, "Item/purchases.html", {'purchases': purchases, 'cart_items': cart_items})

def search(request):
    if request.method == "GET":
        title = request.GET.get('title', '')
        items = Item.objects.filter(title__icontains=title, is_sold=False)

    context = {'items' : items,
               'title': title
            }

    return render(request, "Item/search.html", context)

@login_required
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

def showItem(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'Item/showItem.html', {'item': item})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Purchase

@login_required
def buy(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        payment_info = request.POST.get('payment_info')

        # Save the purchase
        purchase = Purchase.objects.create(
            item=item,
            user=request.user,
            name=name,
            number=number,
            email=email,
            payment_info=payment_info
        )

        # Redirect to confirmation page
        return render(request, 'Item/confirmation.html', {'item': item, 'name': name})

    return render(request, 'Item/buy.html', {'item': item})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Purchase

@login_required
def delete_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)  
    purchase.delete()
    return redirect('index')  









