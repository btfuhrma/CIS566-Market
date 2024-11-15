from django.contrib.auth import authenticate, login as auth_login
from Item.models import Cart, Purchase, Item, ItemBuilder


class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance

    def createUser(self, userManager, email, password):
        userManager.create_user(email=email, password=password)

    def login(self, request, email, password):
        user = authenticate(request, email=email, password=password)
        return user
    
    def getCartItems(self, request):
        cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
        return cart_items
    
    def getPurchases(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        return purchases
    
    def searchItem(self, request):
        title = request.GET.get('title', '')
        items = Item.objects.filter(title__icontains=title, is_sold=False)
        return items

    def createItem(self, request):
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        category = request.POST.get('category', '')
        image = request.POST.get('image', '')
        builder = ItemBuilder()
        builder.set_category(category)
        builder.set_description(description)
        builder.set_price(price)
        builder.set_title(title)
        builder.set_sold(False)
        builder.set_user(request.user)
        builder.set_image(image)
        builder.build()