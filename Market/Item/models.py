from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()  # This gets the current user model

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('handmade', 'Handmade'),
        ('collectible', 'Collectible'),
        ('general_market', 'General Market'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', blank=False, null=False)
    addedDate = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)

# Instead of factory method, changed to builder pattern as I looked it up and its easier and more applicable
class ItemBuilder:

    def __init__(self):
        # Setting default values for the builder pattern
        title = 'Title'
        description = 'Item Description'
        price = 0
        category = 'general_market'
        is_sold = False
        image = None
        user = None

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