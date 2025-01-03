
from django.contrib.auth import views as auth_views

from django.urls import path, include

from . import views

urlpatterns = [
    path("createAccount", views.createAccount, name="createAccount"),
    path("login", views.login, name="login"),
    path("createUser", views.createUser, name="createUser"),
    path("loginPage", views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name='logout'),
    path('Item/', include('Item.urls')),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

]

