from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
from .models import ItemBuilder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# Create your views here.

from .models import Item, Purchase, Cart

from .models import Cart

def index(request):
    # Retrieve cart items for the user if authenticated
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, "Item/index.html", {'cart_items': cart_items})




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

from django.contrib import messages
from .models import Item, Cart

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
   
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if created:
        messages.success(request, f"{item.title} has been added to your cart.")
    else:
        messages.info(request, f"{item.title} is already in your cart.")
    
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Item, Cart
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if created:
        messages.success(request, f"{item.title} has been added to your cart.")
    else:
        messages.info(request, f"{item.title} is already in your cart.")
    
   
    return redirect(request.META.get('HTTP_REFERER', 'index'))

from django.shortcuts import get_object_or_404, redirect
from .models import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def delete_from_cart(request, item_id):
 
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    

    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    

    return redirect('index')

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Item, Purchase
from django.contrib.auth.decorators import login_required

@login_required
def buy(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
      
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

        # Send email confirmation
        subject = f"Purchase Confirmation for {item.title}"
        message = f"Dear {name},\n\nThank you for purchasing {item.title}!\n\nOrder Details:\n- Item: {item.title}\n- Price: ${item.price}\n- Phone: {number}\n- Payment Info: {payment_info}\n\nWe will process your order shortly."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

       
        return render(request, 'Item/confirmation.html', {'item': item, 'name': name})

    return render(request, 'Item/buy.html', {'item': item})



