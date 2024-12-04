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
        cart, created = Cart.objects.get_or_create(user=request.user)

        if item not in cart.items.all():
            cart.items.add(item)
            return created

    def deleteFromCart(self, request, itemId):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(Item, id=itemId)

        if item in cart.items.all():
            cart.items.remove(item)

    def recentItems(self):
        recentItems = Item.objects.all().order_by('-addedDate')[:5]
        return recentItems
    
    def getMyItems(self, request):
        myItems = Item.objects.filter(user=request.user)
        return myItems
    
    def deleteItem(self, request, itemId):
        item = get_object_or_404(Item, user=request.user, id=itemId)
        item.delete()


def search(request):
    if request.method == "GET":
        db = DatabaseSingleton()
        items, title = db.searchItem(request)


        page = int(request.GET.get('page', 1))
        
     
        items_per_page = 1

      
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page


        paginated_items = items[start_index:end_index]


        total_pages = (len(items) + items_per_page - 1) // items_per_page 

     
        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if page < total_pages else None

    
        context = {
            'items': paginated_items,
            'title': title,
            'current_page': page,
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
        }

  
        return render(request, "Item/search.html", context)

