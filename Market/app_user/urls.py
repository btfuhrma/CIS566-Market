from django.urls import path

from . import views

urlpatterns = [
    path("createAccount", views.createAccount, name="createAccount"),
    path("login", views.login, name="login"),
    path("createUser", views.createUser, name="createUser")
]