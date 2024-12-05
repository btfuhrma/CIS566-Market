from django.shortcuts import render, redirect
from .models import AppUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from services import DatabaseSingleton
from Item.views import index
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
import string

# Create your views here.
def createAccount(request):
    return render(request, "app_user/create.html")

def loginPage(request):
    return render(request, "app_user/login.html")

def login(request):
    if request.method == "POST":
        db = DatabaseSingleton()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # Authenticate the user
        
        user = db.login(request, email, password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            return index(request)
        else:
            # Invalid login details
            messages.error(request, "Invalid email or password.")
            return render(request, "app_user/login.html")

    return render(request, "app_user/login.html")

def createUser(request):
    if request.method == "POST":
        db = DatabaseSingleton()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        userManager = AppUser.objects
        db.createUser(userManager, email, password)
    return render(request, "app_user/login.html")

def logoutUser(request):
    logout(request)
    return render(request, "Item/index.html")

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