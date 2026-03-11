from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/new/', views.create_order, name='create_order'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.edit_order, name='edit_order'),
    path('orders/<int:pk>/submit/', views.submit_order, name='submit_order'),
    path('orders/<int:pk>/approve/', views.approve_order, name='approve_order'),
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<int:pk>/status/<str:new_status>/', views.change_order_status, name='change_status'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.create_product, name='create_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),

    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/new/', views.create_supplier, name='create_supplier'),
    path('suppliers/<int:pk>/edit/', views.edit_supplier, name='edit_supplier'),

    # API
    path('api/product/<int:pk>/', views.api_product_info, name='api_product'),
]