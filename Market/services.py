from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404
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
        carts = Cart.objects.filter(user=request.user)
        items_in_cart = [cart_item.item for cart_item in carts]
        return items_in_cart
    
    def getPurchases(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        return purchases
    
    def searchItem(self, request):
        title = request.GET.get('title', '')
        items = Item.objects.filter(title__icontains=title, is_sold=False)
        return items, title

    def createItem(self, request):
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        category = request.POST.get('category', '')
        image = request.FILES.get('image')
        builder = ItemBuilder()
        builder.set_category(category)
        builder.set_description(description)
        builder.set_price(price)
        builder.set_title(title)
        builder.set_sold(False)
        builder.set_user(request.user)
        builder.set_image(image)
        builder.build()
    
    def getItem(self,  id):
        item = get_object_or_404(Item, id=id)
        return item
    
    def createPurchase(self, request, itemId):
        item = item = get_object_or_404(Item, id=itemId)
        try:
            item.is_sold = True
            item.save()
        except:
            return f"Item '{item.title}' marked as sold."
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        payment_info = request.POST.get('payment_info')
        
        purchase = Purchase.objects.create(
            item=item,
            user=request.user,
            name=name,
            number=number,
            email=email,
            payment_info=payment_info
        )

    def createPurchaseCart(self, request):
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        payment_info = request.POST.get('payment_info')

        carts = Cart.objects.filter(user=request.user)
        items_in_cart = [cart_item.item for cart_item in carts]
        for item in items_in_cart:
            try:
                item.is_sold = True
                item.save()
            except:
                return f"Item '{item.title}' marked as sold."
            purchase = Purchase.objects.create(
                item=item,
                user=request.user,
                name=name,
                number=number,
                email=email,
                payment_info=payment_info
            )

    def deletePurchase(self, request, purchaseId):
        purchase = get_object_or_404(Purchase, id=purchaseId, user=request.user)  
        purchase.delete()

    def addToCart(self, request, itemId):
        item = get_object_or_404(Item, id=itemId)
        cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
        return created

    def deleteFromCart(self, request, itemId):
        cart_item = get_object_or_404(Cart, user=request.user, id=itemId)
        cart_item.delete()

    def recentItems(self):
        recentItems = Item.objects.all().order_by('-addedDate')[:5]
        return recentItems
    
    def getMyItems(self, request):
        myItems = Item.objects.filter(user=request.user)
        return myItems
    
    def deleteItem(self, request, itemId):
        item = get_object_or_404(Item, user=request.user, id=itemId)
        item.delete()