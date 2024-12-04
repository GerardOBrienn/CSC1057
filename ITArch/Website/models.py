from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY = (
        ('Stationary', 'Stationary'),
        ('Electronics', 'Electronics'),
        ('Food', 'Food'),
    )
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, blank=True)
    quantity = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}--{self.quantity}'

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_ordered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.product.name} ordered by {self.staff.username}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_default_customers(cls):
        user1 = User.objects.create_user(username='johndoe', password='password123', email='johndoe@example.com')
        user2 = User.objects.create_user(username='janedoe', password='password123', email='janedoe@example.com')
        cls.objects.create(user=user1, phone_number='123-456-7890', address='123 Main St')
        cls.objects.create(user=user2, phone_number='987-654-3210', address='456 Oak St')
        
    def __str__(self):
        return self.user.username
