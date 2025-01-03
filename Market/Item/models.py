from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('handmade', 'Handmade'),
        ('collectible', 'Collectible'),
        ('general_market', 'General Market'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', blank=False, null=False)
    addedDate = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)

class ItemBuilder:

    def __init__(self):
       
        self.title = 'Title'
        self.description = 'Item Description'
        self.price = 0
        self.category = 'general_market'
        self.is_sold = False
        self.image = None
        self.user = None

    def set_user(self, user):
        self.user = user
        return self

    def set_sold(self, sold):
        self.is_sold = sold
        return self

    def set_title(self, title):
        self.title = title
        return self

    def set_description(self, description):
        self.description = description
        return self

    def set_price(self, price):
        self.price = price
        return self

    def set_category(self, category):
        self.category = category
        return self
    
    def set_image(self, image):
        self.image = image
        return self

    def build(self):
        return Item.objects.create(
            user = self.user,
            title=self.title,
            description=self.description,
            price=self.price,
            category=self.category,
            is_sold=self.is_sold,
            image=self.image,
        )


class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    payment_info = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"

from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField('Item', related_name='carts')

    def __str__(self):
        item_titles = ", ".join([item.title for item in self.items.all()])
        return f"{self.user.username}'s Cart: {item_titles}"
