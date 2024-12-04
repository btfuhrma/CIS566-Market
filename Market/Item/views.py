from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Item, ItemBuilder, Cart, Purchase
from .models import ItemBuilder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from services import DatabaseSingleton

def index(request):
    db = DatabaseSingleton()
    recent_items = db.recentItems()
    return render(request, "Item/index.html", {"recent_items" : recent_items})

@login_required
def purchases(request):
    db = DatabaseSingleton()
    purchases = db.getPurchases()
    return render(request, "Item/purchases.html", {'purchases': purchases})

def search(request):
    if request.method == "GET":
        db = DatabaseSingleton()
        items, title = db.searchItem(request)

    context = {'items' : items,
               'title': title
            }

    return render(request, "Item/search.html", context)

@login_required
def createItem(request):
    return render(request, "Item/createItem.html")

def create(request):
    if request.method == "POST":
        db = DatabaseSingleton()
        db.createItem(request)
    return render(request, "Item/index.html")

def showItem(request, id):
    db = DatabaseSingleton()
    item = db.getItem(id)
    return render(request, 'Item/showItem.html', {'item': item})

@login_required
def buy(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    items = []
    items.append(item)
    if request.method == 'POST':
      
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        payment_info = request.POST.get('payment_info')

        db = DatabaseSingleton()
        db.createPurchase(request, item_id)

        subject = f"Purchase Confirmation for {item.title}"
        message = f"Dear {name},\n\nThank you for purchasing {item.title}!\n\nOrder Details:\n- Item: {item.title}\n- Price: ${item.price}\n- Phone: {number}\n- Payment Info: {payment_info}\n\nWe will process your order shortly."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

       
        return render(request, 'Item/confirmation.html', {'item': item, 'name': name})
    return render(request, 'Item/buy.html', {'items': items, "price" : item.price})

@login_required
def buyCart(request):
    if request.method == "POST":
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        payment_info = request.POST.get('payment_info')

        db = DatabaseSingleton()
        cartItems = db.getCartItems(request)

        db.createPurchaseCart(request)

        subject = f"Purchase Confirmation for Your Order"
        item_details = "\n".join(
            [f"- {item.item.title}: ${item.item.price}" for item in cartItems]
        )
        total_price = sum(item.item.price for item in cartItems)

        message = (
            f"Dear {name},\n\n"
            f"Thank you for your purchase!\n\n"
            f"Order Details:\n"
            f"{item_details}\n\n"
            f"Total Price: ${total_price}\n"
            f"Phone: {number}\n"
            f"Payment Info: {payment_info}\n\n"
            f"We will process your order shortly.\n\n"
            f"Best regards,\nYour Team"
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'Item/confirmation.html')
    else:
        db = DatabaseSingleton()
        items = db.getCartItems(request)
        price = 0
        for item in items:
            price += item.price
        return render(request, 'Item/buy.html', {'items': items, "price" : price})

@login_required
def delete_purchase(request, purchase_id):
    db = DatabaseSingleton()
    db.deletePurchase(request, purchase_id)
    return redirect('index')  

@login_required
def add_to_cart(request, item_id):
    db = DatabaseSingleton()
    item = db.getItem(item_id)
    
    created = db.addToCart(request, item_id)
    
    if created:
        messages.success(request, f"{item.title} has been added to your cart.")
    else:
        messages.info(request, f"{item.title} is already in your cart.")
    
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def viewCart(request):
    db = DatabaseSingleton()
    items_in_cart = db.getCartItems(request)
    return render(request, "Item/cart.html", {"cartItems" : items_in_cart})

@login_required
def delete_from_cart(request, item_id):
    db = DatabaseSingleton()
    db.deleteFromCart(request, item_id)
    messages.success(request, "Item removed from your cart.")

    return viewCart(request)

@login_required
def myItems(request):
    db = DatabaseSingleton()
    myItems = db.getMyItems(request)

    return render(request, "Item/myItems.html", {"items" : myItems})

@login_required
def deleteItem(request, item_id):
    db = DatabaseSingleton()
    db.deleteItem(request, item_id)
    messages.success(request, "Item removed from your cart.")
    myItems = db.getMyItems(request)

    return render(request, "Item/myItems.html", {"items" : myItems})

@login_required
def editItem(request, item_id):
    if request.method == "POST":
        pass



def search(request):
    if request.method == "GET":
        db = DatabaseSingleton()
        items, title = db.searchItem(request)

        page = request.GET.get('page', 1)
        
      
        items_per_page = 1

        start_index = (int(page) - 1) * items_per_page
        end_index = start_index + items_per_page

      
        paginated_items = items[start_index:end_index]

     
        total_pages = (len(items) + items_per_page - 1) // items_per_page  

    
        previous_page = int(page) - 1 if int(page) > 1 else None
        next_page = int(page) + 1 if int(page) < total_pages else None

        context = {
            'items': paginated_items,
            'title': title,
            'current_page': int(page),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
        }

    return render(request, "Item/search.html", context)



