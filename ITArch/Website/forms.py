from django import forms
from .models import Product, Order, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user', 'phone_number', 'address']