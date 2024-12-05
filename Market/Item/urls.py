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
    path("purchases", views.purchases, name="purchases"),  
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("delete_from_cart/<int:item_id>/", views.delete_from_cart, name="delete_from_cart"),
    path("viewCart", views.viewCart, name="viewCart"),
    path("buyCart", views.buyCart, name="buyCart"),
    path("myItems", views.myItems, name="myItems"),
    path("deleteItem/<int:item_id>", views.deleteItem, name="deleteItem"),




    
]

