from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, Order, Customer

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity')
    list_filter = ['category']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'staff', 'order_quantity', 'status', 'date_ordered')
    list_filter = ('status', 'staff')
    search_fields = ['product__name', 'staff__username']
    ordering = ('-date_ordered',)

# Register the Customer model to allow managing customer-related fields
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ['user__username']

# Register the models
admin.site.site_header = 'OneOne Dashboard'
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)

# Optionally register the User model if you need to manage users directly
