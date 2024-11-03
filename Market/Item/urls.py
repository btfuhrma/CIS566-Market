from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("createItem", views.createItem, name="createItem"),
    path("create", views.create, name="create"),
    path('item/<int:id>/', views.showItem, name='showItem'),
    path('buy/<int:item_id>/', views.buy, name='buy'),
     path('delete_purchase/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
     


     
]