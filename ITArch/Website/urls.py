from django.urls import path, include
from . import views

urlpatterns = [
    # Homepage and Login
    path('', views.homepage, name='homepage'),  # Homepage URL
    path('login/', views.custom_login, name='user-login'),  # Login URL
    path('accounts/logout/', views.logout_view, name='logout'),
    # Staff-related pages
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/<int:id>/', views.staff_detail, name='dashboard-staff-detail'),

    # Product-related pages
    path('products/', views.product, name='dashboard-product'),
    path('products/<int:id>/delete/', views.product_delete, name='dashboard-product-delete'),
    path('products/<int:id>/update/', views.product_update, name='dashboard-product-update'),

    # Order-related pages
    path('orders/', views.order, name='dashboard-order'),
    path('track-order/<int:id>/', views.track_order, name='dashboard-track-order'),
    path('order/delete/<int:id>/', views.delete_order, name='dashboard-order-delete'),

    # Customer-related pages
    path('customers/', views.customer_list, name='customer-list'),
    path('customers/<int:id>/', views.customer_detail, name='customer-detail'),
    path('customers/create/', views.customer_create, name='customer-create'),
    path('customer-homepage/', views.customer_homepage, name='customer-homepage'),
    
    # Basket page (unfinished)
    path('basket/', views.basket, name='dashboard-basket'),

    # Role-based redirection after login
    path('role-home/', views.role_based_home, name='role-home'),  # Redirect based on user role
    path('__debug__/', include('debug_toolbar.urls')),
    path('dashboard/', views.dashboard_view, name='dashboard-index'),
]
