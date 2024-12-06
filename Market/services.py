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
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        return cart_items
    
    def getPurchases(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        return purchases
    
    def searchItem(self, request):
        title = request.GET.get('title', '')
        category = request.GET.get('category', '')
        items = Item.objects.filter(title__icontains=title, is_sold=False)
        if len(category) > 0 and category != 'all':
            items = items.filter(category=category)
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
        item = get_object_or_404(Item, id=itemId)
        if request.user != item.user:
            try:
                item.is_sold = True
                item.save()
            except:
                return f"Item '{item.title}' marked as sold."
            name = request.POST.get('name')
            number = request.POST.get('number')
            email = request.POST.get('email')
            payment_info = request.POST.get('payment_info')
            address = request.POST.get("address")
            
            purchase = Purchase.objects.create(
                item=item,
                user=request.user,
                name=name,
                number=number,
                email=email,
                payment_info=payment_info,
                address = address
            )
            return True
        return False

    def createPurchaseCart(self, request):
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        payment_info = request.POST.get('payment_info')
        address = request.POST.get("address")

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
                payment_info=payment_info,
                address = address
            )

    def deletePurchase(self, request, purchaseId):
        purchase = get_object_or_404(Purchase, id=purchaseId, user=request.user)  
        purchase.delete()

    def addToCart(self, request, itemId):
        item = get_object_or_404(Item, id=itemId)
        cart, created = Cart.objects.get_or_create(user=request.user)

        if item not in cart.items.all() and request.user != item.user:
            cart.items.add(item)
            return created

    def deleteFromCart(self, request, itemId):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(Item, id=itemId)

        if item in cart.items.all():
            cart.items.remove(item)

    def recentItems(self):
        recentItems = Item.objects.filter(is_sold=False).order_by('-addedDate')[:4]
        return recentItems
    
    def getMyItems(self, request):
        myItems = Item.objects.filter(user=request.user, is_sold=False)
        return myItems
    
    def deleteItem(self, request, itemId):
        item = get_object_or_404(Item, user=request.user, id=itemId)
        item.delete()

    def getMySales(self, request):
        myItems = Item.objects.filter(user=request.user, is_sold=True)
        purchases = Purchase.objects.all()
        purchases = []
        for item in myItems:
            purchase = {}
            saleUser = Purchase.objects.get(item=item)
            purchase["title"] = item.title
            purchase["description"] = item.description
            purchase["price"] = item.price
            purchase["user"] = saleUser.user.email
            purchase["address"] = saleUser.address
            purchase["image"] = item.image.url
            purchases.append(purchase)
        return purchases

class Iterator:
    def __init__(self, items, items_per_page):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 1

    def getNextItems(self):
 
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        
        if start_index < len(self.items):
           
            self.current_page += 1
            return self.items[start_index:end_index]
        else:
            return [] 

    def getPreviousItems(self):
        if self.current_page > 1:
            self.current_page -= 1

       
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page

        return self.items[start_index:end_index]

    def getCurrentPageItems(self):
        
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return self.items[start_index:end_index]

    def getCurrentPage(self):
        return self.current_page

    def getTotalPages(self):
       
        return (len(self.items) + self.items_per_page - 1) // self.items_per_page


