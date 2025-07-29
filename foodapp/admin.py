from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FoodItem, Category, Order  # Import all models you want to manage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

admin.site.register(FoodItem)
admin.site.register(Order)