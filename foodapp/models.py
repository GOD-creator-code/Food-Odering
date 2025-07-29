from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    address = models.TextField()
    items = models.ManyToManyField(FoodItem)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    ordered_at = models.DateTimeField(default=timezone.now)
    
    is_ready = models.BooleanField(default=False)  # Added field to track order status

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
