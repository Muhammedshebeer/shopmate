from django.contrib import admin
from django.urls import path
from . import views 
from .views import clear_orders

urlpatterns = [
    path('home',views.home , name='home'),
    # path('analyze',views.analyzed , name='analyze'),
    path('add-products/', views.add_product, name='add_product'),
    path('header/', views.header, name='header'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('productpage', views.Product_page, name='productpage'),
    # path('title/', views.title, name='title ')
    path('cart_view/', views.cart_view, name='cart_view'),
    # path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    # path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('admin/clear-orders/',clear_orders, name='admin-clear-orders'),
    path('products/', views.all_products_view, name='all_products'),
    # path('products/', views.product_list, name='product_list'),
    # path('delete/', views.delete_data, name='delete'),
    
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout_view, name='checkout'),
    # path('order-success/', views.order_success, name='order-success'),
    path('profile/', views.profile_view, name='profile'),
    # path("create_order/", views.create_order, name="create_order"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("success/", views.success_page, name="success"),
    
    
]