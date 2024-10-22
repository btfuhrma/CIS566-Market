from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # This gets the current user model

# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', blank=False, null=False)
    addedDate = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)