from django import forms
from .models import Order, FoodItem

class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=FoodItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'address', 'items']
