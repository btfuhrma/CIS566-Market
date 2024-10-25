from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("createAccount", views.createAccount, name="createAccount"),
    path("login", views.login, name="login"),
    path("createUser", views.createUser, name="createUser"),
    path("loginPage", views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name='logout'),
]