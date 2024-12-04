from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .models import Product, Order, Customer
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, OrderForm, CustomerForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.conf import settings


# Home Page for Customers
def customer_homepage(request):
    products = Product.objects.all()
    return render(request, 'dashboard/homepage.html', {'products': products})

@login_required(login_url='user-login')
def homepage(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    order_count = Order.objects.count()
    product_count = products.count()
    workers_count = User.objects.count()

    context = {
        'orders': orders,
        'products': products,
        'order_count': order_count,
        'product_count': product_count,
        'workers_count': workers_count,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'dashboard/index.html', context)


# Login View for Users
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user role
            if user.is_staff:
                return redirect('dashboard-index')  # Redirect staff to dashboard
            else:
                return redirect('customer-homepage')  # Redirect customers to their homepage
    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('user-login') 

# Dashboard for Admins (Staff) 
@login_required(login_url='user-login')
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    order_count = Order.objects.count()
    product_count = products.count()
    workers_count = User.objects.count()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'order_count': order_count,
        'product_count': product_count,
        'workers_count': workers_count,
    }
    return render(request, 'dashboard/index.html', context)

# Staff Management Pages
@login_required(login_url='user-login')
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    order_count = Order.objects.count()
    product_count = Product.objects.count()

    context = {
        'workers': workers,
        'workers_count': workers_count,
        'order_count': order_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, id):
    worker = get_object_or_404(User, id=id)
    context = {'worker': worker}
    return render(request, 'dashboard/staff_detail.html', context)

# Product Management Pages
@login_required(login_url='user-login')
def product(request):
    items = Product.objects.all()
    product_count = items.count()
    workers_count = User.objects.count()
    order_count = Order.objects.count()
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been successfully added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'order_count': order_count,
        'product_count': product_count
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, id):
    item = Product.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required
def product_update(request, id):
    item = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {'form': form}
    return render(request, 'dashboard/product_update.html', context)

# Order Management Pages
@login_required(login_url='user-login')
def order(request):
    orders = Order.objects.all()
    order_count = orders.count()
    workers_count = User.objects.count()
    product_count = Product.objects.count()
    if order_count == 0:
        # Example mock orders
        product1 = Product.objects.first()  # Get first product or create mock product if needed
        product2 = Product.objects.last()  # Get last product or use another if you prefer

        # Check if products exist, otherwise create mock products
        if not product1:
            product1 = Product.objects.create(name="Example Product 1", price=25.00, quantity=100)
        if not product2:
            product2 = Product.objects.create(name="Example Product 2", price=40.00, quantity=50)

        # Create mock orders
        Order.objects.create(
            product=product1,
            staff=request.user,
            order_quantity=2,
            status='Shipped',
            date_ordered='2024-12-01'
        )

        Order.objects.create(
            product=product2,
            staff=request.user,
            order_quantity=1,
            status='Pending',
            date_ordered='2024-12-02'
        )

        # Re-fetch orders after adding mock orders
        orders = Order.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-order')
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'workers_count': workers_count,
        'order_count': order_count,
        'product_count': product_count,
        'form': form
    }

    return render(request, 'dashboard/order.html', context)

# Basket Page (to be completed)
@login_required(login_url='user-login')
def basket(request):
    orders = Order.objects.all()
    order_count = orders.count()
    workers_count = User.objects.count()
    product_count = Product.objects.count()
    
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'order_count': order_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/basket.html', context)

# Track Order Page
@login_required
def track_order(request, id):
    try:
        worker = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse("Worker not found.", status=404)

    tracking_id = request.GET.get('tracking_id', None)

    if tracking_id:
        try:
            order = Order.objects.get(tracking_id=tracking_id)
            context = {
                'worker': worker,
                'tracking_id': tracking_id,
                'product_name': order.product.name,
                'order_quantity': order.order_quantity,
                'order_status': order.order_status,
                'delivery_date': order.delivery_date,
                'success': True,
            }
        except Order.DoesNotExist:
            context = {
                'worker': worker,
                'tracking_id': tracking_id,
                'error': 'Tracking ID not found.',
                'success': False,
            }
    else:
        context = {
            'worker': worker,
            'error': 'Tracking ID not provided.',
            'success': False,
        }

    return render(request, 'dashboard/track_order.html', context)

def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()  # Delete the order from the database
    return redirect('dashboard-order') 


# Customer Pages
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    print(customers)
    return render(request, 'dashboard/customers/customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'dashboard/customers/customer_detail.html', {'customer': customer})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customer-list')
    else:
        form = CustomerForm()

    users = User.objects.exclude(customer__isnull=False)  # Users without a Customer profile
    return render(request, 'dashboard/customers/customer_create.html', {'form': form, 'users': users})

# Role-Based Redirect After Login
@login_required
def role_based_home(request):
    if request.user.is_staff:
        return redirect('dashboard-index')  # Redirect staff to dashboard
    else:
        return redirect('customer-homepage')  # Redirect customers to their homepage

@login_required(login_url='user-login')
def dashboard_view(request):
    # Logic for dashboard (similar to your index view)
    orders = Order.objects.all()
    products = Product.objects.all()
    order_count = Order.objects.count()
    product_count = products.count()
    workers_count = User.objects.count()

    context = {
        'orders': orders,
        'products': products,
        'order_count': order_count,
        'product_count': product_count,
        'workers_count': workers_count,
    }

    return render(request, 'dashboard/index.html', context)