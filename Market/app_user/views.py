from django.shortcuts import render, redirect
from .models import AppUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from services import DatabaseSingleton
from Item.views import index

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