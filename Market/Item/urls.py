from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("createItem", views.createItem, name="createItem"),
    path("create", views.create, name="create")
]