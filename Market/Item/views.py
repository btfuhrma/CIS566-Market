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

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages

def createUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')


        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'app_user/create_user.html')

        try:
          
            user = get_user_model().objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'User created successfully.')
            return redirect('login') 
        
        except Exception as e:
            messages.error(request, f'An error occurred while creating the user: {str(e)}')
            return render(request, 'app_user/create_user.html')

    return render(request, 'app_user/create_user.html')


def index(request):
    db = DatabaseSingleton()
    recent_items = db.recentItems()
    return render(request, "Item/index.html", {"recent_items" : recent_items})

@login_required
def purchases(request):
    db = DatabaseSingleton()

    db.getPurchases(request)
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
from services import Iterator  

def search(request):
    if request.method == "GET":
        db = DatabaseSingleton()
        items, title = db.searchItem(request)

      
        items_per_page = 1  
        iterator = Iterator(items, items_per_page)

      
        page = int(request.GET.get('page', 1))

      
        iterator.current_page = page

       
        paginated_items = iterator.getCurrentPageItems()

     
        total_pages = iterator.getTotalPages()

     
        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if page < total_pages else None

     
        context = {
            'items': paginated_items,
            'title': title,
            'current_page': page,
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
        }

      
        return render(request, "Item/search.html", context)

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
import string


def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.error(request, 'No user with this email address exists.')
            return render(request, 'app_user/forgot_password.html')

    
        temp_password = generate_temp_password()

   
        user.set_password(temp_password)
        user.save()

      
        subject = 'Your New Password'
        message = f'Your new password is: {temp_password}\n\nPlease use this to log in and change your password.'

      
        send_mail(
            subject, 
            message,  
            'lilacsabri7@gmail.com',  
            [user.email],  
            fail_silently=False
        )

        messages.success(request, 'A temporary password has been sent to your email. Please go back to the login page and login using your new password.')
        return render(request, 'app_user/forgot_password.html')

    return render(request, 'app_user/forgot_password.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

           
            if user.check_password('temporary_password'):  
             
                return redirect('password_reset_confirmation')

        
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('loginPage')  
    else:
        form = AuthenticationForm()
    return render(request, 'app_user/login.html', {'form': form})


def password_reset_confirmation(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save() 
            update_session_auth_hash(request, form.user)  
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')  
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'app_user/password_reset_confirmation.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def profile_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) 
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'app_user/profile_settings.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def profile_settings(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

     
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('profile_settings')

    
        user = request.user
        user.email = email
        if password:
            user.set_password(password)
        
        user.save()

     
        update_session_auth_hash(request, user)

        messages.success(request, "Profile updated successfully.")
        return redirect('index')  
    
   
    return render(request, 'app_user/profile_settings.html')
